from curation.remodeling.util.base import is_number, get_indices, tuple_to_range, match_label, find_next, \
    split_consecutive_parts
from curation.remodeling.util.bidsfiles import find_task_files,  rename_and_save_new, load_operations

from .remodeling.operations.add_structure_column_op import AddStructureColumnOp
from .remodeling.operations.add_structure_events_op import AddStructureEventsOp
from .remodeling.operations.number_rows_op import NumberRowsOp
from .remodeling.operations.number_groups_op import NumberGroupsOp
from .remodeling.operations.remap_columns_op import RemapColumnsOp
from .remodeling.operations.factor_column_op import FactorColumnOp
from .remodeling.operations.factor_hed_tags_op import FactorHedTagsOp
from .remodeling.operations.factor_hed_type_op import FactorHedTypeOp
from .remodeling.operations.merge_consecutive_op import MergeConsecutiveOp
from .remodeling.operations.remove_columns_op import RemoveColumnsOp
from .remodeling.operations.remove_rows_op import RemoveRowsOp
from .remodeling.operations.rename_columns_op import RenameColumnsOp
from .remodeling.operations.reorder_columns_op import ReorderColumnsOp
from .remodeling.operations.split_event_op import SplitEventOp
from .remodeling.operations.dispatcher import Dispatcher
from . import _version
__version__ = _version.get_versions()['version']
