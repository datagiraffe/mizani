from __future__ import division

import pytest
import numpy as np
import numpy.testing as npt


from ..palettes import (hls_palette, husl_palette, rescale_pal,
                        area_pal, abs_area, grey_pal, hue_pal,
                        brewer_pal, gradient_n_pal, cmap_pal,
                        desaturate_pal)


def test_hls_palette():
    colors = hls_palette(10)
    assert len(colors) == 10
    assert all(len(c) == 3 for c in colors)


def test_husl_palette():
    colors = husl_palette(5)
    assert len(colors) == 5
    assert all(len(c) == 3 for c in colors)


def test_rescale_pal():
    palette = rescale_pal()
    x = np.arange(0, 1+.01, 0.1)
    result = palette(x)
    assert min(result) == 0.1
    assert max(result) == 1

    palette = rescale_pal((20, 100))
    result = palette(x)
    assert min(result) == 20
    assert max(result) == 100


def test_area_pal():
    palette = area_pal((0, 10))
    x = np.arange(0, 11)
    xsq = (x * .1)**2
    result = palette(xsq)
    npt.assert_allclose(result, x)


def test_abs_area():
    x = np.arange(0, 1.03, .1)**2
    palette = abs_area(5)
    result = palette(x)
    assert min(result) == 0
    assert max(result) == 5


def test_grey_pal():
    palette = grey_pal()
    result = palette(5)
    # Same rgb values
    assert all(s[1:3]*3 == s[1:] for s in result)


def test_hue_pal():
    palette = hue_pal()
    result = palette(5)
    assert all(s[0] == '#' and len(s) == 7 for s in result)

    # branches #
    with pytest.raises(ValueError):
        hue_pal(.1, 2.3, 3)

    with pytest.raises(ValueError):
        hue_pal(color_space='slh')


def test_brewer_pal():
    result = brewer_pal()(5)
    assert all(s[0] == '#' and len(s) == 7 for s in result)

    result = brewer_pal('qual', 2)(5)
    assert all(s[0] == '#' and len(s) == 7 for s in result)

    result = brewer_pal('div', 2)(5)
    assert all(s[0] == '#' and len(s) == 7 for s in result)

    with pytest.raises(ValueError):
        brewer_pal('div', 200)(5)

    result = brewer_pal('seq', 'Greens')(5)
    assert all(s[0] == '#' and len(s) == 7 for s in result)

    with pytest.warns(UserWarning):
        brewer_pal()(100)


def test_gradient_n_pal():
    palette = gradient_n_pal(['red', 'blue'])
    result = palette([0, .25, .5, .75, 1])
    assert result[0].lower() == '#ff0000'
    assert result[-1].lower() == '#0000ff'
    assert palette(0).lower() == '#ff0000'

    # symmetric gradient
    palette = gradient_n_pal(['red', 'blue', 'red'], [0, 0.5, 1])
    result = palette([0.2, 0.8])
    assert result[0] == result[1]


def test_cmap_pal():
    palette = cmap_pal('viridis')
    result = palette([0, .25, .5, .75, 1])
    assert all(s[0] == '#' and len(s) == 7 for s in result)


def test_desaturate_pal():
    x = [0, .25, .5, .75, 1]
    # When desaturating pure red, green and blue
    # the other 2 colors get matching values,
    # we test that.
    result = desaturate_pal('red', .1)(x)
    assert all(s[3:5] == s[5:] for s in result)

    result = desaturate_pal('green', .2)(x)
    assert all(s[1:3] == s[-2:] for s in result)

    result = desaturate_pal('blue', .3)(x)
    assert all(s[1:3] == s[3:5] for s in result)

    result = desaturate_pal('blue', .3, reverse=True)(x)
    assert all(s[1:3] == s[3:5] for s in result)

    with pytest.raises(ValueError):
        desaturate_pal('green', 2.3)