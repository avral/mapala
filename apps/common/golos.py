from piston.steem import Steem
from piston.account import Account
from pistonbase import operations
from piston.exceptions import AccountExistsException


class Golos(Steem):
    def create_account(self,
                       account_name,
                       json_meta={},
                       creator=None,
                       owner_key=None,
                       active_key=None,
                       posting_key=None,
                       memo_key=None,
                       password=None,
                       additional_owner_keys=[],
                       additional_active_keys=[],
                       additional_posting_keys=[],
                       additional_owner_accounts=[],
                       additional_active_accounts=[],
                       additional_posting_accounts=[],
                       storekeys=True,
                       ):
        """ Create new account in Steem
            The brainkey/password can be used to recover all generated keys (see
            `steembase.account` for more details.
            By default, this call will use ``default_author`` to
            register a new name ``account_name`` with all keys being
            derived from a new brain key that will be returned. The
            corresponding keys will automatically be installed in the
            wallet.
            .. note:: Account creations cost a fee that is defined by
                       the network. If you create an account, you will
                       need to pay for that fee!
            .. warning:: Don't call this method unless you know what
                          you are doing! Be sure to understand what this
                          method does and where to find the private keys
                          for your account.
            .. note:: Please note that this imports private keys
                      (if password is present) into the wallet by
                      default. However, it **does not import the owner
                      key** for security reasons. Do NOT expect to be
                      able to recover it from the wallet if you lose
                      your password!
            :param str account_name: (**required**) new account name
            :param str json_meta: Optional meta data for the account
            :param str creator: which account should pay the registration fee
                                (defaults to ``default_author``)
            :param str owner_key: Main owner key
            :param str active_key: Main active key
            :param str posting_key: Main posting key
            :param str memo_key: Main memo_key
            :param str password: Alternatively to providing keys, one
                                 can provide a password from which the
                                 keys will be derived
            :param array additional_owner_keys:  Additional owner public keys
            :param array additional_active_keys: Additional active public keys
            :param array additional_posting_keys: Additional posting public keys
            :param array additional_owner_accounts: Additional owner account names
            :param array additional_active_accounts: Additional acctive account names
            :param array additional_posting_accounts: Additional posting account names
            :param bool storekeys: Store new keys in the wallet (default: ``True``)
            :raises AccountExistsException: if the account already exists on the blockchain
        """
        assert len(account_name) <= 16, "Account name must be at most 16 chars long"

        if not creator:
            raise ValueError(
                "Not creator account given. Define it with " +
                "creator=x, or set the default_author using piston")
        if password and (owner_key or posting_key or active_key or memo_key):
            raise ValueError(
                "You cannot use 'password' AND provide keys!"
            )

        account = None
        try:
            account = Account(account_name)
        except:
            pass
        if account:
            raise AccountExistsException

        " Generate new keys from password"
        from pistonbase.account import PasswordKey, PublicKey
        if password:
            posting_key = PasswordKey(account_name, password, role="posting")
            active_key = PasswordKey(account_name, password, role="active")
            owner_key = PasswordKey(account_name, password, role="owner")
            memo_key = PasswordKey(account_name, password, role="memo")
            posting_pubkey = posting_key.get_public_key()
            active_pubkey = active_key.get_public_key()
            owner_pubkey = owner_key.get_public_key()
            memo_pubkey = memo_key.get_public_key()
            posting_privkey = posting_key.get_private_key()
            active_privkey = active_key.get_private_key()
            # owner_privkey   = owner_key.get_private_key()
            memo_privkey = memo_key.get_private_key()
            # store private keys
            if storekeys:
                # self.wallet.addPrivateKey(owner_privkey)
                self.wallet.addPrivateKey(active_privkey)
                self.wallet.addPrivateKey(posting_privkey)
                self.wallet.addPrivateKey(memo_privkey)
        elif (owner_key and posting_key and active_key and memo_key):
            posting_pubkey = PublicKey(posting_key, prefix=self.rpc.chain_params["prefix"])
            active_pubkey = PublicKey(active_key, prefix=self.rpc.chain_params["prefix"])
            owner_pubkey = PublicKey(owner_key, prefix=self.rpc.chain_params["prefix"])
            memo_pubkey = PublicKey(memo_key, prefix=self.rpc.chain_params["prefix"])
        else:
            raise ValueError(
                "Call incomplete! Provide either a password or public keys!"
            )

        owner = format(owner_pubkey, self.rpc.chain_params["prefix"])
        active = format(active_pubkey, self.rpc.chain_params["prefix"])
        posting = format(posting_pubkey, self.rpc.chain_params["prefix"])
        memo = format(memo_pubkey, self.rpc.chain_params["prefix"])

        owner_key_authority = [[owner, 1]]
        active_key_authority = [[active, 1]]
        posting_key_authority = [[posting, 1]]
        owner_accounts_authority = []
        active_accounts_authority = []
        posting_accounts_authority = []

        # additional authorities
        for k in additional_owner_keys:
            owner_key_authority.append([k, 1])
        for k in additional_active_keys:
            active_key_authority.append([k, 1])
        for k in additional_posting_keys:
            posting_key_authority.append([k, 1])

        for k in additional_owner_accounts:
            owner_accounts_authority.append([k, 1])
        for k in additional_active_accounts:
            active_accounts_authority.append([k, 1])
        for k in additional_posting_accounts:
            posting_accounts_authority.append([k, 1])

        props = self.rpc.get_chain_properties()
        fee = props["account_creation_fee"]
        s = {'creator': creator,
             'fee': fee,
             'json_metadata': json_meta,
             'memo_key': memo,
             'new_account_name': account_name,
             'owner': {'account_auths': owner_accounts_authority,
                       'key_auths': owner_key_authority,
                       'weight_threshold': 1},
             'active': {'account_auths': active_accounts_authority,
                        'key_auths': active_key_authority,
                        'weight_threshold': 1},
             'posting': {'account_auths': posting_accounts_authority,
                         'key_auths': posting_key_authority,
                         'weight_threshold': 1},
             'prefix': self.rpc.chain_params["prefix"]}

        op = operations.Account_create(**s)

        return self.finalizeOp(op, creator, "active")
