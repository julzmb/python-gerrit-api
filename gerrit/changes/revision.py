#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Author: Jialiang Shi
from urllib.parse import quote
from gerrit.changes.drafts import Drafts
from gerrit.changes.comments import Comments
from gerrit.changes.files import Files


class Revision:
    def __init__(self, project, change, revision, gerrit):
        self.project = project
        self.change = change
        self.revision = revision
        self.gerrit = gerrit

    def get_commit(self):
        """
        Retrieves a parsed commit of a revision.

        :return:
        """
        endpoint = "/changes/%s/revisions/%s/commit" % (self.change, self.revision)
        response = self.gerrit.requester.get(self.gerrit.get_endpoint_url(endpoint))
        result = self.gerrit.decode_response(response)
        return self.gerrit.projects.get(self.project).get_commit(result.get("commit"))

    def get_description(self) -> str:
        """
        Retrieves the description of a patch set.
        If the patch set does not have a description an empty string is returned.

        :return:
        """
        endpoint = "/changes/%s/revisions/%s/description" % (self.change, self.revision)
        response = self.gerrit.requester.get(self.gerrit.get_endpoint_url(endpoint))
        result = self.gerrit.decode_response(response)
        return result

    def set_description(self, input_: dict) -> str:
        """
        Sets the description of a patch set.

        :param input_: the DescriptionInput entity
        :return:
        """
        endpoint = "/changes/%s/revisions/%s/description" % (self.change, self.revision)
        base_url = self.gerrit.get_endpoint_url(endpoint)
        response = self.gerrit.requester.put(
            base_url, json=input_, headers=self.gerrit.default_headers
        )
        result = self.gerrit.decode_response(response)
        return result

    def get_merge_list(self) -> list:
        """
        Returns the list of commits that are being integrated into a target branch by a merge commit.
        By default the first parent is assumed to be uninteresting. By using the parent option another
        parent can be set as uninteresting (parents are 1-based).

        :return:
        """
        endpoint = "/changes/%s/revisions/%s/mergelist" % (self.change, self.revision)
        response = self.gerrit.requester.get(self.gerrit.get_endpoint_url(endpoint))
        result = self.gerrit.decode_response(response)
        return [
            self.gerrit.projects.get(self.project).get_commit(item.get("commit"))
            for item in result
        ]

    def get_revision_actions(self) -> dict:
        """
        Retrieves revision actions of the revision of a change.

        :return:
        """
        endpoint = "/changes/%s/revisions/%s/actions" % (self.change, self.revision)
        response = self.gerrit.requester.get(self.gerrit.get_endpoint_url(endpoint))
        result = self.gerrit.decode_response(response)
        return result

    def get_review(self) -> dict:
        """
        Retrieves a review of a revision.

        :return:
        """
        endpoint = "/changes/%s/revisions/%s/review" % (self.change, self.revision)
        response = self.gerrit.requester.get(self.gerrit.get_endpoint_url(endpoint))
        result = self.gerrit.decode_response(response)
        return result

    def get_related_changes(self) -> dict:
        """
        Retrieves related changes of a revision. Related changes are changes that either depend on,
        or are dependencies of the revision.

        :return:
        """
        endpoint = "/changes/%s/revisions/%s/related" % (self.change, self.revision)
        response = self.gerrit.requester.get(self.gerrit.get_endpoint_url(endpoint))
        result = self.gerrit.decode_response(response)
        return result

    def set_review(self, input_: dict) -> dict:
        """
        Sets a review on a revision, optionally also publishing draft comments, setting labels, adding reviewers or CCs,
        and modifying the work in progress property.
        A review cannot be set on a change edit. Trying to post a review for a change edit fails with 409 Conflict.

        :param input_: the ReviewInput entity
        :return:
        """
        endpoint = "/changes/%s/revisions/%s/review" % (self.change, self.revision)
        base_url = self.gerrit.get_endpoint_url(endpoint)
        response = self.gerrit.requester.post(
            base_url, json=input_, headers=self.gerrit.default_headers
        )
        result = self.gerrit.decode_response(response)
        return result

    def rebase(self, input_: dict) -> dict:
        """
        Rebases a revision.
        Optionally, the parent revision can be changed to another patch set through the RebaseInput entity.

        :param input_: the RebaseInput entity
        :return:
        """
        endpoint = "/changes/%s/revisions/%s/rebase" % (self.change, self.revision)
        base_url = self.gerrit.get_endpoint_url(endpoint)
        response = self.gerrit.requester.post(
            base_url, json=input_, headers=self.gerrit.default_headers
        )
        result = self.gerrit.decode_response(response)
        return result

    def submit(self) -> dict:
        """
        Submits a revision.
        If the revision cannot be submitted, e.g. because the submit rule doesn’t allow submitting the revision or the
        revision is not the current revision, the response is 409 Conflict and the error message is contained in the
        response body.

        :return:
        """
        endpoint = "/changes/%s/revisions/%s/submit" % (self.change, self.revision)
        response = self.gerrit.requester.post(self.gerrit.get_endpoint_url(endpoint))
        result = self.gerrit.decode_response(response)
        return result

    def get_patch(self, zip=False, download=False, path=None):
        """
        Gets the formatted patch for one revision.
        The formatted patch is returned as text encoded inside base64

        Adding query parameter zip (for example /changes/…​/patch?zip) returns the patch as a single file inside of a
        ZIP archive. Clients can expand the ZIP to obtain the plain text patch, avoiding the need for a base64 decoding
        step. This option implies download.

        Query parameter download (e.g. /changes/…​/patch?download) will suggest the browser save the patch as
        commitsha1.diff.base64, for later processing by command line tools.

        If the path parameter is set, the returned content is a diff of the single file that the path refers to.

        :return:
        """
        endpoint = "/changes/%s/revisions/%s/patch" % (self.change, self.revision)

        if zip:
            endpoint += endpoint + "?zip"

        if download:
            endpoint += endpoint + "?download"

        if path:
            endpoint += endpoint + "?path=%s" % quote(path, safe="")

        response = self.gerrit.requester.get(self.gerrit.get_endpoint_url(endpoint))
        result = self.gerrit.decode_response(response)
        return result

    def submit_preview(self):
        """
        need fix bug
        Gets a file containing thin bundles of all modified projects if this change was submitted.

        :return:
        """
        endpoint = "/changes/%s/revisions/%s/preview_submit" % (
            self.change,
            self.revision,
        )
        response = self.gerrit.requester.get(self.gerrit.get_endpoint_url(endpoint))
        result = self.gerrit.decode_response(response)
        return result

    def is_mergeable(self) -> dict:
        """
        Gets the method the server will use to submit (merge) the change and an indicator if the change is currently mergeable.

        :return:
        """
        endpoint = "/changes/%s/revisions/%s/mergeable" % (self.change, self.revision)
        response = self.gerrit.requester.get(self.gerrit.get_endpoint_url(endpoint))
        result = self.gerrit.decode_response(response)
        return result

    def get_submit_type(self) -> str:
        """
        Gets the method the server will use to submit (merge) the change.

        :return:
        """
        endpoint = "/changes/%s/revisions/%s/submit_type" % (self.change, self.revision)
        response = self.gerrit.requester.get(self.gerrit.get_endpoint_url(endpoint))
        result = self.gerrit.decode_response(response)
        return result

    def test_submit_type(self, input_: str):
        """
        Tests the submit_type Prolog rule in the project, or the one given.

        :param input_: the Prolog code
        :return:
        """
        endpoint = "/changes/%s/revisions/%s/test.submit_type" % (
            self.change,
            self.revision,
        )
        base_url = self.gerrit.get_endpoint_url(endpoint)
        response = self.gerrit.requester.post(
            base_url, data=input_, headers={"Content-Type": "plain/text"}
        )
        result = self.gerrit.decode_response(response)
        return result

    def test_submit_rule(self, input_: str):
        """
        Tests the submit_rule Prolog rule in the project, or the one given.

        :param input_: the Prolog code
        :return:
        """
        endpoint = "/changes/%s/revisions/%s/test.submit_rule" % (
            self.change,
            self.revision,
        )
        base_url = self.gerrit.get_endpoint_url(endpoint)
        response = self.gerrit.requester.post(
            base_url, data=input_, headers={"Content-Type": "plain/text"}
        )
        result = self.gerrit.decode_response(response)
        return result

    @property
    def drafts(self):
        return Drafts(change=self.change, revision=self.revision, gerrit=self.gerrit)

    @property
    def comments(self):
        return Comments(change=self.change, revision=self.revision, gerrit=self.gerrit)

    @property
    def files(self):
        return Files(change=self.change, revision=self.revision, gerrit=self.gerrit)

    def cherry_pick(self, input_: dict):
        """
        Cherry picks a revision to a destination branch.

        :param input_: the CherryPickInput entity
        :return:
        """
        endpoint = "/changes/%s/revisions/%s/cherrypick" % (self.change, self.revision)
        base_url = self.gerrit.get_endpoint_url(endpoint)
        response = self.gerrit.requester.post(
            base_url, json=input_, headers=self.gerrit.default_headers
        )
        result = self.gerrit.decode_response(response)
        return result

    def list_reviewers(self):
        """
        Lists the reviewers of a revision.

        :return:
        """
        endpoint = "/changes/%s/revisions/%s/reviewers" % (self.change, self.revision)
        response = self.gerrit.requester.get(self.gerrit.get_endpoint_url(endpoint))
        result = self.gerrit.decode_response(response)
        return result