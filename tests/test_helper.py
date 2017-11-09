"""
Contains several testing helper function
"""

import pytest
import numpy as np


def _plugin_import(plug):
    import sys
    if sys.version_info >= (3, 4):
        from importlib import util
        plug_spec = util.find_spec(plug)
    else:
        import pkgutil
        plug_spec = pkgutil.find_loader(plug)
    if plug_spec is None:
        return False
    else:
        return True


def is_psi4_new_enough(version_feature_introduced):
    if not _plugin_import('psi4'):
        return False
    import psi4
    from pkg_resources import parse_version
    #print(psi4.__file__)
    #print(psi4.__version__)
    #print(parse_version(psi4.__version__))
    #print(parse_version(version_feature_introduced))
    return parse_version(psi4.__version__) >= parse_version(version_feature_introduced)

using_psi4_libxc = pytest.mark.skipif(is_psi4_new_enough("1.2a1.dev100") is False,
                                reason="Psi4 does not include DFT rewrite to use Libxc. Update to development head")


def compare_collocation_results(test, ref):
    if set(test) != set(ref):
        raise KeyError("Test and Ref results dicts do not match")

    for k in ref.keys():
        match = np.allclose(test[k], ref[k])
        if not match:
            raise ValueError("Test and Ref results do not match for %s" % k)