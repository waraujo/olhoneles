# -*- coding: utf-8 -*-
#
# Copyright (©) 2014, Marcelo Jorge Vieira <metal@alucinados.com>
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU Affero General Public License as
#  published by the Free Software Foundation, either version 3 of the
#  License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU Affero General Public License for more details.
#
#  You should have received a copy of the GNU Affero General Public License
#  along with this program.  If not, see <http://www.gnu.org/licenses/>.

from datetime import datetime, timedelta

from django.core.management.base import CommandError
from django.core.management import call_command
from django.test import TestCase
from mock import patch, call

from montanha.tests.fixtures import (
    InstitutionFactory, LegislatureFactory, CollectionRunFactory
)


class CollectCommandsTestCase(TestCase):

    def _create_institution(self, siglum):
        institution = InstitutionFactory.create(name=siglum, siglum=siglum)
        date_start = datetime.now()
        date_end = date_start + timedelta(days=365 * 4)
        self.legislature = LegislatureFactory.create(
            date_start=date_start, date_end=date_end, institution=institution
        )

    def test_command_collect_without_institution(self):
        with self.assertRaises(CommandError):
            call_command('collect')

    @patch('montanha.management.commands.collect.Command.collection_runs')
    @patch('montanha.management.commands.collect.call_command')
    @patch('montanha.management.commands.collectors.almg.ALMG')
    def test_with_institution_almg(
            self, mock_institution, mock_call_command, collection_runs_mock):

        self._create_institution('ALMG')

        collection_run = CollectionRunFactory.create()
        collection_runs_mock.__iter__.return_value = [collection_run]

        call_command('collect', 'almg')

        self.assertIn(call().update_legislators(), mock_institution.mock_calls)
        self.assertIn(call().update_data(), mock_institution.mock_calls)
        self.assertIn(call().update_legislators_data(), mock_institution.mock_calls)
        self.assertEqual(
            mock_call_command.mock_calls, [call('consolidate', 'almg')]
        )

    @patch('montanha.management.commands.collect.Command.collection_runs')
    @patch('montanha.management.commands.collect.call_command')
    @patch('montanha.management.commands.collectors.algo.ALGO')
    def test_with_institution_algo(
            self, mock_institution, mock_call_command, collection_runs_mock):

        self._create_institution('ALGO')

        collection_run = CollectionRunFactory.create()
        collection_runs_mock.__iter__.return_value = [collection_run]

        call_command('collect', 'algo')

        self.assertIn(call().update_legislators(), mock_institution.mock_calls)
        self.assertIn(call().update_data(), mock_institution.mock_calls)
        self.assertEqual(
            mock_call_command.mock_calls, [call('consolidate', 'algo')]
        )

    @patch('montanha.management.commands.collect.Command.collection_runs')
    @patch('montanha.management.commands.collect.call_command')
    @patch('montanha.management.commands.collectors.senado.Senado')
    def test_with_institution_senado(
            self, mock_institution, mock_call_command, collection_runs_mock):

        self._create_institution('SENADO')

        collection_run = CollectionRunFactory.create()
        collection_runs_mock.__iter__.return_value = [collection_run]

        call_command('collect', 'senado')

        self.assertIn(call().update_data(), mock_institution.mock_calls)
        self.assertEqual(
            mock_call_command.mock_calls, [call('consolidate', 'senado')]
        )

    @patch('montanha.management.commands.collect.Command.collection_runs')
    @patch('montanha.management.commands.collect.call_command')
    @patch('montanha.management.commands.collectors.cmbh.CMBH')
    def test_with_institution_cmbh(
            self, mock_institution, mock_call_command, collection_runs_mock):

        self._create_institution('CMBH')

        collection_run = CollectionRunFactory.create()
        collection_runs_mock.__iter__.return_value = [collection_run]

        call_command('collect', 'cmbh')

        self.assertIn(call().update_legislators(), mock_institution.mock_calls)
        self.assertIn(call().update_data(), mock_institution.mock_calls)
        self.assertEqual(
            mock_call_command.mock_calls, [call('consolidate', 'cmbh')]
        )

    @patch('montanha.management.commands.collect.Command.collection_runs')
    @patch('montanha.management.commands.collect.call_command')
    @patch('montanha.management.commands.collectors.cmsp.CMSP')
    def test_with_institution_cmsp(
            self, mock_institution, mock_call_command, collection_runs_mock):

        self._create_institution('CMSP')

        collection_run = CollectionRunFactory.create()
        collection_runs_mock.__iter__.return_value = [collection_run]

        call_command('collect', 'cmsp')

        self.assertIn(call().update_data(), mock_institution.mock_calls)
        self.assertEqual(
            mock_call_command.mock_calls, [call('consolidate', 'cmsp')]
        )

    @patch('montanha.management.commands.collect.Command.collection_runs')
    @patch('montanha.management.commands.collect.call_command')
    @patch('montanha.management.commands.collectors.cdep.CamaraDosDeputados')
    def test_with_institution_cdep(
            self, mock_institution, mock_call_command, collection_runs_mock):

        self._create_institution('CamaraDosDeputados')

        collection_run = CollectionRunFactory.create()
        collection_runs_mock.__iter__.return_value = [collection_run]

        call_command('collect', 'cdep')

        self.assertIn(call().update_data(), mock_institution.mock_calls)
        self.assertEqual(
            mock_call_command.mock_calls, [call('consolidate', 'cdep')]
        )
