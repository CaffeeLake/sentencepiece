from typing import Any, Literal, Sequence, overload

__version__: str

_OutType = type[int] | type[str] | Literal["serialized_proto", "proto", "immutable_proto"]
_DecodeOutType = type[str] | type[bytes] | Literal["serialized_proto", "immutable_proto"]


class ImmutableSentencePieceText_ImmutableSentencePiece:
    @property
    def piece(self) -> str: ...
    @property
    def id(self) -> int: ...


class ImmutableSentencePieceText:
    @property
    def text(self) -> str: ...
    @property
    def pieces(self) -> Sequence[ImmutableSentencePieceText_ImmutableSentencePiece]: ...
    def SerializeAsString(self) -> bytes: ...


class SentencePieceProcessor:
    def __init__(
        self,
        model_file: str | None = ...,
        model_proto: bytes | None = ...,
        out_type: type[int] | type[str] = ...,
        add_bos: bool = ...,
        add_eos: bool = ...,
        reverse: bool = ...,
        emit_unk_piece: bool = ...,
        enable_sampling: bool = ...,
        nbest_size: int = ...,
        alpha: float = ...,
        num_threads: int = ...,
    ) -> None: ...

    def Load(self, model_file: str | None = ..., model_proto: bytes | None = ...) -> bool: ...
    def LoadFromFile(self, arg: str) -> bool: ...
    def LoadFromSerializedProto(self, serialized: bytes) -> bool: ...

    def GetPieceSize(self) -> int: ...
    @overload
    def PieceToId(self, piece: str) -> int: ...
    @overload
    def PieceToId(self, piece: Sequence[str]) -> list[int]: ...
    @overload
    def IdToPiece(self, id: int) -> str: ...
    @overload
    def IdToPiece(self, id: Sequence[int]) -> list[str]: ...

    def Encode(
        self,
        input: str | Sequence[str],
        out_type: _OutType | None = ...,
        add_bos: bool | None = ...,
        add_eos: bool | None = ...,
        reverse: bool | None = ...,
        emit_unk_piece: bool | None = ...,
        enable_sampling: bool | None = ...,
        nbest_size: int | None = ...,
        alpha: float | None = ...,
        num_threads: int | None = ...,
    ) -> Any: ...
    def EncodeAsIds(self, input: str | Sequence[str], **kwargs: Any) -> Any: ...
    def EncodeAsPieces(self, input: str | Sequence[str], **kwargs: Any) -> Any: ...
    def Decode(
        self,
        input: int | str | Sequence[int] | Sequence[str] | Sequence[Sequence[int]] | Sequence[Sequence[str]],
        out_type: _DecodeOutType = ...,
        num_threads: int | None = ...,
    ) -> Any: ...
    def DecodeIds(self, input: int | Sequence[int] | Sequence[Sequence[int]], **kwargs: Any) -> Any: ...
