from curation.remodeling.util.base import is_number, get_indices, tuple_to_range, match_label, find_next, \
    split_consecutive_parts
from curation.remodeling.util.bidsfiles import find_task_files, replace_new_with_old, \
    rename_and_save_new, load_operations
from .operations.dispatcher import Dispatcher
from .operations.add_structure_column_op import AddStructureColumnOp
from .operations.add_structure_events_op import AddStructureEventsOp
from .operations.number_rows_op import NumberRowsOp
from .operations.remap_columns_op import RemapColumnsOp
from .operations.factor_column_op import FactorColumnOp
from .operations.factor_hed_tags_op import FactorHedTagsOp
from .operations.factor_hed_type_op import FactorHedTypeOp
from .operations.merge_consecutive_op import MergeConsecutiveOp
from .operations.remove_columns_op import RemoveColumnsOp
from .operations.reorder_columns_op import ReorderColumnsOp
from .operations.rename_columns_op import RenameColumnsOp
from .operations.split_event_op import SplitEventOp