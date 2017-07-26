import ecdsa
import hashlib
from binascii import unhexlify

from graphenebase import PublicKey
from bitshares.bitshares import BitShares

from backend.settings import DACOM_NODE_WSS


class AccountDoesNotExist(Exception):
    pass


def _recover_public_key(digest, signature, i):
    """ Recover the public key from the the signature """
    # See: //www.secg.org/download/aid-780/sec1-v2.pdf section 4.1.6 primarily
    curve = ecdsa.SECP256k1.curve
    G = ecdsa.SECP256k1.generator
    order = ecdsa.SECP256k1.order
    yp = (i % 2)
    r, s = ecdsa.util.sigdecode_string(signature, order)
    x = r + (i // 2) * order
    alpha = ((x * x * x) + (curve.a() * x) + curve.b()) % curve.p()
    beta = ecdsa.numbertheory.square_root_mod_prime(alpha, curve.p())
    y = beta if (beta - yp) % 2 == 0 else curve.p() - beta
    # 1.4 Constructor of Point is supposed to check if nR is at infinity.
    R = ecdsa.ellipticcurve.Point(curve, x, y, order)
    # 1.5 Compute e
    e = ecdsa.util.string_to_number(digest)
    # 1.6 Compute Q = r^-1(sR - eG)
    Q = ecdsa.numbertheory.inverse_mod(r, order) * (s * R + (-e % order) * G)
    # Not strictly necessary, but let's verify the message for paranoia's sake.
    if not ecdsa.VerifyingKey.from_public_point(
        Q, curve=ecdsa.SECP256k1
    ).verify_digest(signature, digest, sigdecode=ecdsa.util.sigdecode_string):
        return None

    return ecdsa.VerifyingKey.from_public_point(Q, curve=ecdsa.SECP256k1)


def verify_signature(accUsername, auth_sig_hash, auth_sig):
    dacom = BitShares(DACOM_NODE_WSS)
    account = dacom.rpc.get_account(accUsername)
    signature = unhexlify(auth_sig)

    pub = PublicKey(account['active']['key_auths'][0][0], 'FLO')

    vk = ecdsa.VerifyingKey.from_public_point(
        pub.point(),
        curve=ecdsa.SECP256k1
    )

    sig = bytes(signature)[1:]
    recoverParameter = (bytes(signature)[0]) - 4 - 27
    digest = hashlib.sha256(auth_sig_hash).digest()
    # digest = hashlib.sha256(b'sdf').digest()

    p = _recover_public_key(digest, sig, recoverParameter)

    if p.to_der() != vk.to_der():
        raise ValueError()
