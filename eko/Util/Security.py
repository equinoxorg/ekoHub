from eko.ThirdParty.baseconv import BaseConverter

from os.path import exists, isfile

import Crypto.PublicKey.RSA as RSA
import Crypto.Hash.MD5 as MD5

import logging

logger = logging.getLogger('eko.Util.Security')

def load_RSA(keypath):
    if (exists(keypath) and isfile(keypath)):
        try:
            fh = open(keypath, 'r')
            key = RSA.importKey(fh.read())
        except IOError:
            logger.exception("Public Key file not found! (Path %s)" % keypath)
            exit(-100)
        except (ValueError, IndexError, TypeError):
            logger.exception("Import Public Key failed! (Path %s)" % keypath)
            fh.close()
            exit(-101)
        fh.close()
    else:
        logger.warn("No primary key object!")
        key = False
    return key

def solve_challenge(challenge, keypath):
    baseconv = BaseConverter('0123456789abcdef')
    key = load_RSA(keypath)
    if key:
        try:
            signature = key.sign(challenge, "")
            sig_encoded = baseconv.from_decimal(signature[0])
        except :
            logger.exception("Unable to sign challenge with RSA.")
            return ''
    else:
        return ''
    return sig_encoded

def sign_digest(digest, keypath):
    baseconv = BaseConverter('0123456789abcdef')
    key = load_RSA(keypath)
    try:
        return baseconv.from_decimal(key.sign(digest, "")[0])
    except:
        logger.exception("Unable to sign MD5 hash digest with RSA.")
        return ''