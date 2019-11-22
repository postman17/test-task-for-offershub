from django.db import models

from utils.asana_api import AsanaApiWrapper


class ProjectModel(models.Model):
    gid = models.BigIntegerField('Gid', blank=True, null=True)
    name = models.CharField('Name', max_length=100)

    class Meta:
        verbose_name = 'Project'
        verbose_name_plural = 'Projects'

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.gid:
            self.gid = AsanaApiWrapper().create_project(self.name)
        else:
            AsanaApiWrapper().update_project(self.gid, self.name)
        super(ProjectModel, self).save(*args, **kwargs)


class UserModel(models.Model):
    gid = models.BigIntegerField('Gid')
    name = models.CharField('Name', max_length=100)

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        AsanaApiWrapper().add_user_to_workspace(self.gid)
        super(UserModel, self).save(*args, **kwargs)


class TaskModel(models.Model):
    gid = models.BigIntegerField('Gid',blank=True, null=True)
    project = models.ForeignKey('ProjectModel', on_delete=models.CASCADE)
    user = models.ForeignKey('UserModel', on_delete=models.CASCADE)
    text = models.TextField('Text')

    class Meta:
        verbose_name = 'Task'
        verbose_name_plural = 'Tasks'

    def __str__(self):
        return str(self.gid)

    def save(self, *args, **kwargs):
        if not self.gid:
            self.gid = AsanaApiWrapper().create_task(self.project.gid, self.user.gid, self.text)
        else:
            AsanaApiWrapper().update_task(self.gid, self.text, self.project.gid, self.user.gid)
        super(TaskModel, self).save(*args, **kwargs)
