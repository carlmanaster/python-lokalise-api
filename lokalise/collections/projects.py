from ..models.project import ProjectModel


class ProjectsCollection:
    DATA_KEY = "projects"

    def __init__(self, raw_data):
        raw_items = raw_data[self.DATA_KEY]
        self.items = []
        for item in raw_items:
            self.items.append(ProjectModel(item))

        pagination = raw_data.get("_pagination", {})
        if pagination:
            self.total_count = int(pagination.get(
                "x-pagination-total-count", 0))
            self.page_count = int(pagination.get("x-pagination-page-count", 0))
            self.limit = int(pagination.get("x-pagination-limit", 0))
            self.current_page = int(pagination.get("x-pagination-page", 0))

    def is_last_page(self):
        return not self.has_next_page()

    def is_first_page(self):
        return not self.has_prev_page()

    def has_next_page(self):
        return self.current_page > 0 and self.current_page < self.page_count

    def has_prev_page(self):
        return self.current_page > 1
