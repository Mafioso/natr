from django.db import models


class ProjectQuerySet(models.QuerySet):

	def by_project(self, project_id):
		return self.filter(project__id=project_id)




class ProjectBasedModel(models.Model):

	class Meta:
		abstract = True

	objects = ProjectQuerySet.as_manager()

