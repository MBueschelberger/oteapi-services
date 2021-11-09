# pylint: disable=W0613, W0511
"""
Transformation plugin for compevo usecase (fetch output and print it)
"""

from typing import Dict, Optional, Any
from dataclasses import dataclass
from app.models.transformationconfig import TransformationConfig
from app.strategy.factory import StrategyFactory
import dlite


@dataclass
@StrategyFactory.register(("transformation_type", "dlite/compevo-result"))
class CompevoTransformation:
    """Transformations"""

    transformation_config: TransformationConfig

    def initialize(self, session: Optional[Dict[str, Any]] = None) -> Dict:
        """Initialize a job"""
        coll = dlite.Collection()
        dlite.get_collection(coll.uuid)
        return dict(collection_id=coll.uuid)

    def get(self, session: Optional[Dict[str, Any]] = None) -> Dict:
        """Fetch result and print"""

        coll = dlite.get_collection(session["collection_id"])
        pf = coll.get("pore_fraction")
        print("Pore fraction: %.1f%%" % (100 * pf.pore_fraction))

        return dict(PoreFraction="Pore fraction: %.1f%%" % (100 * pf.pore_fraction))
