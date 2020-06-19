"""
lokalise.client
~~~~~~~~~~~~~~~
This module contains API client definition.
"""
from typing import Any, Optional, Union, Dict, Callable, List
import importlib
from lokalise.utils import snake_to_camel
from .collections.branches import BranchesCollection
from .collections.comments import CommentsCollection
from .collections.contributors import ContributorsCollection
from .collections.files import FilesCollection
from .collections.projects import ProjectsCollection
from .collections.queued_processes import QueuedProcessesCollection
from .collections.languages import LanguagesCollection
from .models.branch import BranchModel
from .models.comment import CommentModel
from .models.contributor import ContributorModel
from .models.project import ProjectModel
from .models.queued_process import QueuedProcessModel
from .models.language import LanguageModel


class Client:
    """Client used to send API requests.

    Usage:

        import lokalise
        client = lokalise.Client('api_token')
        client.projects()
    """

    def __init__(
            self,
            token: str,
            connect_timeout: Optional[Union[int, float]] = None,
            read_timeout: Optional[Union[int, float]] = None) -> None:
        """Instantiate a new Lokalise API client.

        :param token: Your Lokalise API token.
        :param connect_timeout: (optional) Server connection timeout
        (the value is in seconds). By default, the client will wait indefinitely.
        :type connect_timeout: int or float
        :param read_timeout: (optional) Server read timeout
        (the value is in seconds). By default, the client will wait indefinitely.
        :type read_timeout: int or float
        """
        self.token = token
        self.connect_timeout = connect_timeout
        self.read_timeout = read_timeout

    def reset_client(self) -> None:
        """Resets the API client by clearing all attributes.
        """
        self.token = ''
        self.connect_timeout = None
        self.read_timeout = None
        self.__clear_endpoint_attrs()

    # === Endpoint methods ===
    def branches(self,
                 project_id: str,
                 params: Optional[Dict[str, Union[int, str]]] = None
                 ) -> BranchesCollection:
        """Fetches all branches for the given project.

        :param str project_id: ID of the project to fetch branches for.
        :param dict params: (optional) Pagination params
        :return: Collection of branches
        """
        raw_branches = self.get_endpoint("branches"). \
            all(parent_id=project_id, params=params)
        return BranchesCollection(raw_branches)

    def branch(self,
               project_id: str,
               branch_id: Union[str, int]) -> BranchModel:
        """Fetches a single branch.

        :param str project_id: ID of the project
        :param branch_id: ID of the branch to fetch
        :type branch_id: int or str
        :return: Branch model
        """
        raw_branch = self.get_endpoint("branches"). \
            find(parent_id=project_id, resource_id=branch_id)
        return BranchModel(raw_branch)

    def create_branch(self,
                      project_id: str,
                      params: Dict[str, str]
                      ) -> BranchModel:
        """Creates a new branch inside the project

        :param str project_id: ID of the project
        :param dict params: Branch parameters
        :return: Branch model
        """
        raw_branch = self.get_endpoint("branches"). \
            create(params, parent_id=project_id)

        return BranchModel(raw_branch)

    def update_branch(self,
                      project_id: str,
                      branch_id: Union[str, int],
                      params: Dict[str, str]) -> BranchModel:
        """Updates a branch.

        :param str project_id: ID of the project
        :param branch_id: ID of the branch to update
        :type branch_id: int or str
        :param dict params: Update parameters
        :return: Branch model
        """
        raw_branch = self.get_endpoint("branches"). \
            update(params, parent_id=project_id, resource_id=branch_id)
        return BranchModel(raw_branch)

    def delete_branch(self, project_id: str,
                      branch_id: Union[str, int]) -> Dict:
        """Deletes a branch.

        :param str project_id: ID of the project
        :param branch_id: ID of the branch to delete
        :type branch_id: int or str
        :return: Dictionary with project ID and "branch_deleted" set to True
        :rtype dict:
        """
        response = self.get_endpoint("branches"). \
            delete(parent_id=project_id, resource_id=branch_id)
        return response

    def merge_branch(self, project_id: str,
                     branch_id: Union[str, int],
                     params: Optional[Dict[str, Union[str, int]]] = None
                     ) -> Dict:
        """Merges a branch.

        :param str project_id: ID of the project
        :param branch_id: ID of the source branch
        :type branch_id: int or str
        :param dict params: Merge parameters
        :return: Dictionary with project ID, "branch_merged" set to True, and branches info
        :rtype dict:
        """
        response = self.get_endpoint("branches"). \
            merge(params, parent_id=project_id, resource_id=branch_id)
        response['branch'] = BranchModel(response['branch'])
        response['target_branch'] = BranchModel(response['target_branch'])
        return response

    def project_comments(self,
                         project_id: str,
                         params: Optional[Dict[str, Union[int, str]]] = None
                         ) -> CommentsCollection:
        """Fetches all comments for the given project.

        :param str project_id: ID of the project to fetch comments for.
        :param dict params: (optional) Pagination params
        :return: Collection of comments
        """
        raw_comments = self.get_endpoint("project_comments"). \
            all(parent_id=project_id, params=params)
        return CommentsCollection(raw_comments)

    def key_comments(self,
                     project_id: str,
                     key_id: Union[str, int],
                     params: Optional[Dict[str, Union[int, str]]] = None
                     ) -> CommentsCollection:
        """Fetches all comments for the given key inside a project.

        :param str project_id: ID of the project
        :param key_id: ID of key to fetch comments for
        :type key_id: int or str
        :param dict params: (optional) Pagination params
        :return: Collection of comments
        """
        raw_comments = self.get_endpoint("key_comments"). \
            all(parent_id=project_id, resource_id=key_id, params=params)
        return CommentsCollection(raw_comments)

    def key_comment(self,
                    project_id: str,
                    key_id: Union[str, int],
                    comment_id: Union[str, int]
                    ) -> CommentModel:
        """Fetches a single comment for a given key.

        :param str project_id: ID of the project
        :param key_id: ID of key to fetch comments for
        :type key_id: int or str
        :param comment_id: Comment identifier to fetch
        :type comment_id: int or str
        :return: Comment model
        """
        raw_comment = self.get_endpoint("key_comments").find(
            parent_id=project_id,
            resource_id=key_id,
            subresource_id=comment_id
        )
        return CommentModel(raw_comment)

    def create_key_comments(self,
                            project_id: str,
                            key_id: Union[str, int],
                            params: Union[List[Dict], Dict[str, str]]
                            ) -> CommentsCollection:
        """Creates one or more comments for the given key.

        :param str project_id: ID of the project
        :param key_id: ID of key to create comments for
        :type key_id: int or str
        :param params: Comment parameters
        :type params: list or dict
        :return: Collection of comments
        """
        raw_comments = self.get_endpoint("key_comments").create(
            params,
            wrapper_attr="comments",
            parent_id=project_id,
            resource_id=key_id
        )
        return CommentsCollection(raw_comments)

    def delete_key_comment(self,
                           project_id: str,
                           key_id: Union[str, int],
                           comment_id: Union[str, int]
                           ) -> Dict:
        """Deletes a given key comment.

        :param str project_id: ID of the project
        :param key_id: ID of key to delete comment for.
        :type key_id: int or str
        :param comment_id: Comment to delete
        :type comment_id: int or str
        :return: Dictionary with project ID and "comment_deleted" set to True
        """
        response = self.get_endpoint("key_comments").delete(
            parent_id=project_id,
            resource_id=key_id,
            subresource_id=comment_id
        )
        return response

    def contributors(self,
                     project_id: str,
                     params: Optional[Dict[str, Union[int, str]]] = None
                     ) -> ContributorsCollection:
        """Fetches all contributors for the given project.

        :param str project_id: ID of the project to fetch contributors for.
        :param dict params: (optional) Pagination params
        :return: Collection of contributors
        """
        raw_contributors = self.get_endpoint("contributors"). \
            all(parent_id=project_id, params=params)
        return ContributorsCollection(raw_contributors)

    def contributor(self,
                    project_id: str,
                    contributor_id: Union[str, int]) -> ContributorModel:
        """Fetches a single contributor.

        :param str project_id: ID of the project
        :param contributor_id: ID of the contributor to fetch
        :type contributor_id: int or str
        :return: Contributor model
        """
        raw_contributor = self.get_endpoint("contributors"). \
            find(parent_id=project_id, resource_id=contributor_id)
        return ContributorModel(raw_contributor)

    def create_contributors(self,
                            project_id: str,
                            params: Union[Dict[str, Any], List[Dict]]
                            ) -> ContributorsCollection:
        """Creates one or more contributors inside the project

        :param str project_id: ID of the project
        :param params: Contributors parameters
        :type params: list or dict
        :return: Contributors collection
        """
        raw_contributors = self.get_endpoint("contributors"). \
            create(params, wrapper_attr="contributors", parent_id=project_id)

        return ContributorsCollection(raw_contributors)

    def update_contributor(self,
                           project_id: str,
                           contributor_id: Union[str, int],
                           params: Dict[str, Any]) -> ContributorModel:
        """Updates a single contributor.

        :param str project_id: ID of the project
        :param contributor_id: ID of the contributor to update
        :type contributor_id: int or str
        :param dict params: Update parameters
        :return: Contributor model
        """
        raw_contributor = self.get_endpoint("contributors"). \
            update(params, parent_id=project_id, resource_id=contributor_id)
        return ContributorModel(raw_contributor)

    def delete_contributor(self, project_id: str,
                           contributor_id: Union[str, int]) -> Dict:
        """Deletes a contributor.

        :param str project_id: ID of the project
        :param contributor_id: ID of the contributor to delete
        :type contributor_id: int or str
        :return: Dictionary with project ID and "contributor_deleted" set to True
        :rtype dict:
        """
        response = self.get_endpoint("contributors"). \
            delete(parent_id=project_id, resource_id=contributor_id)
        return response

    def files(self,
              project_id: str,
              params: Optional[Dict[str, Union[int, str]]] = None
              ) -> FilesCollection:
        """Fetches all files for the given project.

        :param str project_id: ID of the project to fetch files for.
        :param dict params: (optional) Pagination params
        :return: Collection of files
        """
        raw_files = self.get_endpoint("files"). \
            all(parent_id=project_id, params=params)
        return FilesCollection(raw_files)

    def upload_file(self, project_id: str,
                    params: Dict[str, Any]) -> QueuedProcessModel:
        """Uploads a file to the given project.

        :param str project_id: ID of the project to upload file to
        :param dict params: Upload params
        :return: Queued process model
        """
        raw_process = self.get_endpoint("files"). \
            upload(params, parent_id=project_id)
        return QueuedProcessModel(raw_process)

    def download_files(self, project_id: str,
                       params: Dict[str, Any]) -> Dict:
        """Downloads files from the given project.

        :param str project_id: ID of the project to download from
        :param dict params: Download params
        :return: Dictionary with project ID and a bundle URL
        """
        response = self.get_endpoint("files"). \
            download(params, parent_id=project_id)
        return response

    def system_languages(
            self, params: Optional[Dict[str, Union[str, int]]] = None) -> LanguagesCollection:
        """Fetches all languages that Lokalise supports.

        :param dict params: (optional) Pagination params
        :return: Collection of languages
        """
        raw_languages = self.get_endpoint(
            "system_languages").all(params=params)
        return LanguagesCollection(raw_languages)

    def project_languages(self,
                          project_id: str,
                          params: Optional[Dict[str, Union[str, int]]] = None
                          ) -> LanguagesCollection:
        """Fetches all languages for the given project.

        :param str project_id: ID of the project
        :param dict params: (optional) Pagination params
        :return: Collection of languages
        """
        raw_languages = self.get_endpoint("languages"). \
            all(parent_id=project_id, params=params)
        return LanguagesCollection(raw_languages)

    def create_languages(self,
                         project_id: str,
                         params: Dict[str, Any]) -> LanguagesCollection:
        """Create one or more languages for the given project.

        :param str project_id: ID of the project
        :param params: Language parameters
        :type params: dict or list
        :return: Collection of languages
        """
        raw_languages = self.get_endpoint("languages"). \
            create(params, wrapper_attr="languages", parent_id=project_id)
        return LanguagesCollection(raw_languages)

    def language(self,
                 project_id: str,
                 language_id: Union[str, int]) -> LanguageModel:
        """Fetches a project language.

        :param str project_id: ID of the project
        :param language_id: ID of the language to fetch
        :return: Language model
        """
        raw_language = self.get_endpoint("languages"). \
            find(parent_id=project_id, resource_id=language_id)
        return LanguageModel(raw_language)

    def update_language(self,
                        project_id: str,
                        language_id: Union[str, int],
                        params: Dict[str, Any]) -> LanguageModel:
        """Updates a project language.

        :param str project_id: ID of the project
        :param language_id: ID of the language to update
        :param dict params: Update parameters
        :return: Language model
        """
        raw_language = self.get_endpoint("languages"). \
            update(params, parent_id=project_id, resource_id=language_id)
        return LanguageModel(raw_language)

    def delete_language(self, project_id: str,
                        language_id: Union[str, int]) -> Dict:
        """Deletes a project language.

        :param str project_id: ID of the project
        :param language_id: ID of the language to delete
        :return: Dictionary with project ID and "language_deleted" set to True
        :rtype dict:
        """
        response = self.get_endpoint("languages"). \
            delete(parent_id=project_id, resource_id=language_id)
        return response

    def projects(self, params: Optional[str] = None) -> ProjectsCollection:
        """Fetches all projects available to the currently authorized user
        (identified by the API token).

        :param dict params: (optional) Pagination params
        :return: Collection of projects
        """
        raw_projects = self.get_endpoint("projects").all(params=params)
        return ProjectsCollection(raw_projects)

    def project(self, project_id: str) -> ProjectModel:
        """Fetches a single project by ID.

        :param str project_id: ID of the project to fetch
        :return: Project model
        """
        raw_project = self.get_endpoint("projects"). \
            find(parent_id=project_id)
        return ProjectModel(raw_project)

    def create_project(self, params: Dict[str, Any]) -> ProjectModel:
        """Creates a new project.

        :param dict params: Project parameters
        :return: Project model
        """
        raw_project = self.get_endpoint("projects").create(params)
        return ProjectModel(raw_project)

    def update_project(self, project_id: str,
                       params: Dict[str, Any]) -> ProjectModel:
        """Updates a project.

        :param str project_id: ID of the project to update
        :param dict params: Project parameters
        :return: Project model
        """
        raw_project = self.get_endpoint("projects").\
            update(params, parent_id=project_id)
        return ProjectModel(raw_project)

    def empty_project(self, project_id: str) -> Dict:
        """Empties a given project by removing all keys and translations.

        :param str project_id: ID of the project to empty
        :return: Dictionary with the project ID and "keys_deleted" set to True
        :rtype dict:
        """
        return self.get_endpoint("projects").empty(parent_id=project_id)

    def delete_project(self, project_id: str) -> Dict:
        """Deletes a given project.

        :param str project_id: ID of the project to empty
        :return: Dictionary with project ID and "project_deleted" set to True
        :rtype dict:
        """
        return self.get_endpoint("projects").delete(parent_id=project_id)

    def queued_processes(self, project_id: str) -> QueuedProcessesCollection:
        """Fetches all queued processes for the given project.

        :param str project_id: ID of the project
        :return: Collection of queued processes
        """
        raw_processes = self.get_endpoint("queued_processes"). \
            all(parent_id=project_id)
        return QueuedProcessesCollection(raw_processes)

    def queued_process(self,
                       project_id: str,
                       queued_process_id: Union[str, int]) -> QueuedProcessModel:
        """Fetches a queued process.

        :param str project_id: ID of the project
        :param queued_process_id: ID of the process to fetch
        :type queued_process_id: int or str
        :return: Queued process model
        """
        raw_process = self.get_endpoint("queued_processes"). \
            find(parent_id=project_id, resource_id=queued_process_id)
        return QueuedProcessModel(raw_process)
    # === End of endpoint methods ===

    # === Endpoint helpers
    def get_endpoint(self, name: str) -> Any:
        """Lazily loads an endpoint with a given name and stores it
        under a specific instance attribute. For example, if the `name`
        is "projects", then it will load .endpoints.projects_endpoint module
        and then set attribute like this:
            self.__projects_endpoint = ProjectsEndpoint(self)

        :param str name: Endpoint name to load
        """
        endpoint_name = name + "_endpoint"
        camelized_name = snake_to_camel(endpoint_name)
        # Dynamically load the necessary endpoint module
        module = importlib.import_module(
            f".endpoints.{endpoint_name}", package='lokalise')
        # Find endpoint class in the module
        endpoint_klass = getattr(module, camelized_name)
        return self.__fetch_attr(f"__{endpoint_name}",
                                 lambda: endpoint_klass(self))

    def __fetch_attr(self, attr_name: str, populator: Callable) -> Any:
        """Searches for the given attribute. Uses populator
        to set the attribute if it cannot be found. Used to lazy-load
        endpoints.
        """
        if not hasattr(self, attr_name):
            setattr(self, attr_name, populator())

        return getattr(self, attr_name)

    def __clear_endpoint_attrs(self) -> None:
        """Clears all lazily-loaded endpoint attributes
        """
        endpoint_attrs = [a for a in vars(self) if a.endswith('_endpoint')]
        for attr in endpoint_attrs:
            setattr(self, attr, None)
