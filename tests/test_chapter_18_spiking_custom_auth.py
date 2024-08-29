#!/usr/bin/env python3
import os
import unittest

from book_tester import ChapterTest


class Chapter18Test(ChapterTest):
    chapter_name = "chapter_18_spiking_custom_auth"
    previous_chapter = "chapter_17_second_deploy"

    def test_listings_and_commands_and_output(self):
        self.parse_listings()

        # sanity checks
        # self.assertEqual(self.listings[0].type, 'other command')
        self.assertEqual(self.listings[1].type, "code listing with git ref")
        self.assertEqual(self.listings[2].type, "other command")
        # self.assertTrue(self.listings[88].dofirst)

        # skips
        self.skip_with_check(33, "switch back to main")  # comment
        self.skip_with_check(35, "remove any trace")  # comment

        # prep
        self.start_with_checkout()
        self.prep_database()

        # hack fast-forward
        if os.environ.get("SKIP"):
            self.pos = 51
            self.sourcetree.run_command(
                "git checkout {}".format(self.sourcetree.get_commit_spec("ch18l026"))
            )

        while self.pos < len(self.listings):
            print(self.pos)
            self.recognise_listing_and_process_it()

        self.assert_all_listings_checked(self.listings)

        # and do a final commit
        self.sourcetree.run_command('git add . && git commit -m"final commit"')
        self.check_final_diff(ignore=["Generated by Django 4.2"])


if __name__ == "__main__":
    unittest.main()
