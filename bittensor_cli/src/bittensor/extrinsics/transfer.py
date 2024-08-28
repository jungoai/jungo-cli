import asyncio

from bittensor_wallet import Wallet
from rich.prompt import Confirm

from bittensor_cli.src import NETWORK_EXPLORER_MAP
from bittensor_cli.src.subtensor_interface import SubtensorInterface
from bittensor_cli.src.bittensor.balances import Balance
from bittensor_cli.src.utils import (
    console,
    err_console,
    is_valid_bittensor_address_or_public_key,
    get_explorer_url_for_network,
    format_error_message,
)


async def transfer_extrinsic(
    subtensor: SubtensorInterface,
    wallet: Wallet,
    destination: str,
    amount: Balance,
    wait_for_inclusion: bool = True,
    wait_for_finalization: bool = False,
    keep_alive: bool = True,
    prompt: bool = False,
) -> bool:
    """Transfers funds from this wallet to the destination public key address.

    :param subtensor: initialized SubtensorInterface object used for transfer
    :param wallet: Bittensor wallet object to make transfer from.
    :param destination: Destination public key address (ss58_address or ed25519) of recipient.
    :param amount: Amount to stake as Bittensor balance.
    :param wait_for_inclusion: If set, waits for the extrinsic to enter a block before returning `True`,
                               or returns `False` if the extrinsic fails to enter the block within the timeout.
    :param wait_for_finalization:  If set, waits for the extrinsic to be finalized on the chain before returning
                                   `True`, or returns `False` if the extrinsic fails to be finalized within the timeout.
    :param keep_alive: If set, keeps the account alive by keeping the balance above the existential deposit.
    :param prompt: If `True`, the call waits for confirmation from the user before proceeding.
    :return: success: Flag is `True` if extrinsic was finalized or included in the block. If we did not wait for
                      finalization / inclusion, the response is `True`, regardless of its inclusion.
    """

    async def get_transfer_fee() -> Balance:
        """
        Calculates the transaction fee for transferring tokens from a wallet to a specified destination address.
        This function simulates the transfer to estimate the associated cost, taking into account the current
        network conditions and transaction complexity.
        """
        call = await subtensor.substrate.compose_call(
            call_module="Balances",
            call_function="transfer_allow_death",
            call_params={"dest": destination, "value": amount.rao},
        )

        try:
            payment_info = await subtensor.substrate.get_payment_info(
                call=call, keypair=wallet.coldkeypub
            )
        except Exception as e:
            payment_info = {"partialFee": int(2e7)}  # assume  0.02 Tao
            err_console.print(
                f":cross_mark: [red]Failed to get payment info[/red]:[bold white]\n"
                f"  {e}[/bold white]\n"
                f"  Defaulting to default transfer fee: {payment_info['partialFee']}"
            )

        return Balance.from_rao(payment_info["partialFee"])

    async def do_transfer() -> tuple[bool, str, str]:
        """
        Makes transfer from wallet to destination public key address.
        :return: success, block hash, formatted error message
        """
        call = await subtensor.substrate.compose_call(
            call_module="Balances",
            call_function="transfer_allow_death",
            call_params={"dest": destination, "value": amount.rao},
        )
        extrinsic = await subtensor.substrate.create_signed_extrinsic(
            call=call, keypair=wallet.coldkey
        )
        response = await subtensor.substrate.submit_extrinsic(
            extrinsic,
            wait_for_inclusion=wait_for_inclusion,
            wait_for_finalization=wait_for_finalization,
        )
        # We only wait here if we expect finalization.
        if not wait_for_finalization and not wait_for_inclusion:
            return True, "", ""

        # Otherwise continue with finalization.
        response.process_events()
        if response.is_success:
            block_hash_ = response.block_hash
            return True, block_hash_, ""
        else:
            return False, "", format_error_message(response.error_message)

    # Validate destination address.
    if not is_valid_bittensor_address_or_public_key(destination):
        err_console.print(
            f":cross_mark: [red]Invalid destination address[/red]:[bold white]\n  {destination}[/bold white]"
        )
        return False

    # Unlock wallet coldkey.
    wallet.unlock_coldkey()

    # Check balance.
    with console.status(":satellite: Checking balance and fees..."):
        # check existential deposit and fee
        block_hash = await subtensor.substrate.get_chain_head()
        account_balance_, existential_deposit = await asyncio.gather(
            subtensor.get_balance(wallet.coldkey.ss58_address, block_hash=block_hash),
            subtensor.get_existential_deposit(block_hash=block_hash),
        )
        account_balance = account_balance_[wallet.coldkey.ss58_address]
        fee = await get_transfer_fee()

    if not keep_alive:
        # Check if the transfer should keep_alive the account
        existential_deposit = Balance(0)

    # Check if we have enough balance.
    if account_balance < (amount + fee + existential_deposit):
        err_console.print(
            ":cross_mark: [red]Not enough balance[/red]:[bold white]\n"
            f"  balance: {account_balance}\n"
            f"  amount: {amount}\n"
            f"  for fee: {fee}[/bold white]"
        )
        return False

    # Ask before moving on.
    if prompt:
        if not Confirm.ask(
            "Do you want to transfer:[bold white]\n"
            f"  amount: {amount}\n"
            f"  from: {wallet.name}:{wallet.coldkey.ss58_address}\n"
            f"  to: {destination}\n  for fee: {fee}[/bold white]"
        ):
            return False

    with console.status(":satellite: Transferring..."):
        success, block_hash, err_msg = await do_transfer()

        if success:
            console.print(":white_heavy_check_mark: [green]Finalized[/green]")
            console.print(f"[green]Block Hash: {block_hash}[/green]")

            explorer_urls = get_explorer_url_for_network(
                subtensor.network, block_hash, NETWORK_EXPLORER_MAP
            )
            if explorer_urls != {} and explorer_urls:
                console.print(
                    f"[green]Opentensor Explorer Link: {explorer_urls.get('opentensor')}[/green]"
                )
                console.print(
                    f"[green]Taostats Explorer Link: {explorer_urls.get('taostats')}[/green]"
                )
        else:
            console.print(f":cross_mark: [red]Failed[/red]: {err_msg}")

    if success:
        with console.status(":satellite: Checking Balance..."):
            new_balance = await subtensor.get_balance(
                wallet.coldkey.ss58_address, reuse_block=False
            )
            console.print(
                f"Balance:\n"
                f"  [blue]{account_balance[wallet.coldkey.ss58_address]}[/blue] :arrow_right: [green]{new_balance[wallet.coldkey.ss58_address]}[/green]"
            )
            return True

    return False