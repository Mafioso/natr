from django.db import models


class ProjectQuerySet(models.QuerySet):

	def by_project(self, project):
		if isinstance(project, int):
			return self.filter(project__id=project)
		return self.filter(project=project)


class ProjectBasedModel(models.Model):

	class Meta:
		abstract = True

	project = models.ForeignKey('projects.Project', null=True)

	objects = ProjectQuerySet.as_manager()


	def get_project(self):
		return self.project