# global
import paddle
from typing import Optional, Tuple, Union, Any

# local
from ivy.functional.ivy.experimental.linear_algebra import _check_valid_dimension_size
from ivy.func_wrapper import with_unsupported_device_and_dtypes
from ivy.utils.exceptions import IvyNotImplementedException
from .. import backend_version


@with_unsupported_device_and_dtypes(
    {"2.4.2 and below": {"cpu": ("int8", "int16", "uint8", "float16")}}, backend_version
)
def diagflat(
    x: paddle.Tensor,
    /,
    *,
    offset: Optional[int] = 0,
    padding_value: Optional[float] = 0,
    align: Optional[str] = "RIGHT_LEFT",
    num_rows: Optional[int] = None,
    num_cols: Optional[int] = None,
    out: Optional[paddle.Tensor] = None,
):
    diag = paddle.diag(x.flatten(), padding_value=padding_value, offset=offset)
    num_rows = num_rows if num_rows is not None else diag.shape[0]
    num_cols = num_cols if num_cols is not None else diag.shape[1]

    if num_rows < diag.shape[0]:
        diag = diag[:num_rows, :]
    if num_cols < diag.shape[1]:
        diag = diag[:, :num_cols]

    if diag.shape == [num_rows, num_cols]:
        return diag
    else:
        return paddle.nn.Pad2D(
            padding=(0, num_rows - diag.shape[0], 0, num_cols - diag.shape[1]),
            mode="constant",
            value=padding_value,
        )(diag)


@with_unsupported_device_and_dtypes(
    {"2.4.2 and below": {"cpu": ("int8", "uint8", "int16")}}, backend_version
)
def kron(
    a: paddle.Tensor,
    b: paddle.Tensor,
    /,
    *,
    out: Optional[paddle.Tensor] = None,
) -> paddle.Tensor:
    return paddle.kron(a, b)


def matrix_exp(
    x: paddle.Tensor,
    /,
    *,
    out: Optional[paddle.Tensor] = None,
) -> paddle.Tensor:
    # TODO: this is elementwise exp, should be changed to matrix exp ASAP
    return paddle.exp(x)


def eig(
    x: paddle.Tensor, /, *, out: Optional[paddle.Tensor] = None
) -> Tuple[paddle.Tensor]:
    return paddle.linalg.eig(x)


def eigvals(x: paddle.Tensor, /) -> paddle.Tensor:
    return paddle.linalg.eig(x)[0]


def adjoint(
    x: paddle.Tensor,
    /,
    *,
    out: Optional[paddle.Tensor] = None,
) -> paddle.Tensor:
    _check_valid_dimension_size(x)
    return paddle.moveaxis(x, -2, -1).conj()


def cond(
    x: paddle.Tensor,
    /,
    *,
    p: Optional[Union[None, int, str]] = None,
    out: Optional[paddle.Tensor] = None,
) -> Any:
    raise IvyNotImplementedException()


def cov(
    x1: paddle.Tensor,
    x2: paddle.Tensor = None,
    /,
    *,
    rowVar: bool = True,
    bias: bool = False,
    ddof: Optional[int] = None,
    fweights: Optional[paddle.Tensor] = None,
    aweights: Optional[paddle.Tensor] = None,
    dtype: Optional[paddle.dtype] = None,
):
    raise IvyNotImplementedException()
