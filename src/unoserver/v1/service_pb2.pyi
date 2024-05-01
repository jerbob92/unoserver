from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class ConvertRequest(_message.Message):
    __slots__ = ("inpath", "indata", "outpath", "convert_to", "filtername", "filter_options", "update_index", "infiltername")
    INPATH_FIELD_NUMBER: _ClassVar[int]
    INDATA_FIELD_NUMBER: _ClassVar[int]
    OUTPATH_FIELD_NUMBER: _ClassVar[int]
    CONVERT_TO_FIELD_NUMBER: _ClassVar[int]
    FILTERNAME_FIELD_NUMBER: _ClassVar[int]
    FILTER_OPTIONS_FIELD_NUMBER: _ClassVar[int]
    UPDATE_INDEX_FIELD_NUMBER: _ClassVar[int]
    INFILTERNAME_FIELD_NUMBER: _ClassVar[int]
    inpath: str
    indata: bytes
    outpath: str
    convert_to: str
    filtername: str
    filter_options: _containers.RepeatedScalarFieldContainer[str]
    update_index: bool
    infiltername: str
    def __init__(self, inpath: _Optional[str] = ..., indata: _Optional[bytes] = ..., outpath: _Optional[str] = ..., convert_to: _Optional[str] = ..., filtername: _Optional[str] = ..., filter_options: _Optional[_Iterable[str]] = ..., update_index: bool = ..., infiltername: _Optional[str] = ...) -> None: ...

class ConvertResponse(_message.Message):
    __slots__ = ("outdata",)
    OUTDATA_FIELD_NUMBER: _ClassVar[int]
    outdata: bytes
    def __init__(self, outdata: _Optional[bytes] = ...) -> None: ...

class CompareRequest(_message.Message):
    __slots__ = ("oldpath", "olddata", "newpath", "newdata", "outpath", "filetype")
    OLDPATH_FIELD_NUMBER: _ClassVar[int]
    OLDDATA_FIELD_NUMBER: _ClassVar[int]
    NEWPATH_FIELD_NUMBER: _ClassVar[int]
    NEWDATA_FIELD_NUMBER: _ClassVar[int]
    OUTPATH_FIELD_NUMBER: _ClassVar[int]
    FILETYPE_FIELD_NUMBER: _ClassVar[int]
    oldpath: str
    olddata: bytes
    newpath: str
    newdata: bytes
    outpath: str
    filetype: str
    def __init__(self, oldpath: _Optional[str] = ..., olddata: _Optional[bytes] = ..., newpath: _Optional[str] = ..., newdata: _Optional[bytes] = ..., outpath: _Optional[str] = ..., filetype: _Optional[str] = ...) -> None: ...

class CompareResponse(_message.Message):
    __slots__ = ("outdata",)
    OUTDATA_FIELD_NUMBER: _ClassVar[int]
    outdata: bytes
    def __init__(self, outdata: _Optional[bytes] = ...) -> None: ...
