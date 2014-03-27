from piston.handler import BaseHandler
from budget.models import *

class BudgetHandler(BaseHandler):
    model = Budget
    fields = ( 'timestamp', 'description', 'family', ( 'entry_set', ( 'category_id', 'amount_abs', 'payments_per_year' ) ) )

    def read(self, req, *args, **kwargs):
        f = req.user.familymember.families.first()
        return Budget.objects.filter(family = f)
