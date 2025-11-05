from sqlalchemy import Select


class UserScopedServiceMixin:
    async def _apply_user_scope(self, stmt: Select, user_id: int) -> Select:
        model = stmt.column_descriptions[0]["entity"]
        if hasattr(model, "user_id"):
            stmt = stmt.where(model.user_id == user_id)
        return stmt


class SoftDeleteFilterMixin:
    def _apply_soft_delete_filter(
        self, stmt: Select, include_deleted: bool = False
    ) -> Select:
        model = stmt.column_descriptions[0]["entity"]
        if hasattr(model, "is_deleted") and not include_deleted:
            stmt = stmt.where(model.is_deleted == False)
        return stmt
