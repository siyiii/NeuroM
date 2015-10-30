# Copyright (c) 2015, Ecole Polytechnique Federale de Lausanne, Blue Brain Project
# All rights reserved.
#
# This file is part of NeuroM <https://github.com/BlueBrain/NeuroM>
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
#     1. Redistributions of source code must retain the above copyright
#        notice, this list of conditions and the following disclaimer.
#     2. Redistributions in binary form must reproduce the above copyright
#        notice, this list of conditions and the following disclaimer in the
#        documentation and/or other materials provided with the distribution.
#     3. Neither the name of the copyright holder nor the names of
#        its contributors may be used to endorse or promote products
#        derived from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY
# DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
# ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

'''Test neurom.stats

Since the stats module consists of simple wrappers to scipy.stats functions,
these tests are only sanity checks.
'''

from neurom import stats as st
from nose import tools as nt
import numpy as np
import random

np.random.seed(42)

NORMAL_MU = 10.
NORMAL_SIGMA = 1.0
NORMAL = np.random.normal(NORMAL_MU, NORMAL_SIGMA, 1000)

EXPON_LAMBDA = 10.
EXPON = np.random.exponential(EXPON_LAMBDA, 1000)

UNIFORM_MIN = -1.
UNIFORM_MAX = 1.
UNIFORM = np.random.uniform(UNIFORM_MIN, UNIFORM_MAX, 1000)

def test_fit_normal_params():
    fit_ = st.fit(NORMAL, 'norm')
    nt.assert_almost_equal(fit_.params[0], NORMAL_MU, 1)
    nt.assert_almost_equal(fit_.params[1], NORMAL_SIGMA, 1)

def test_fit_normal_dict():
    fit_ = st.fit(NORMAL, 'norm')
    d = st.fit_results_to_dict(fit_, min_bound=-123, max_bound=123)
    nt.assert_almost_equal(d['mu'], NORMAL_MU, 1)
    nt.assert_almost_equal(d['sigma'], NORMAL_SIGMA, 1)
    nt.assert_almost_equal(d['min'], -123, 1)
    nt.assert_almost_equal(d['max'], 123, 1)

def test_fit_normal_regression():
    fit_ = st.fit(NORMAL, 'norm')
    nt.assert_almost_equal(fit_.params[0], 10.019332055822, 12)
    nt.assert_almost_equal(fit_.params[1], 0.978726207747, 12)
    nt.assert_almost_equal(fit_.errs[0], 0.021479979161, 12)
    nt.assert_almost_equal(fit_.errs[1], 0.745431659944, 12)


def test_fit_default_is_normal():
    fit0_ = st.fit(NORMAL)
    fit1_ = st.fit(NORMAL, 'norm')
    nt.assert_items_equal(fit0_.params, fit1_.params)
    nt.assert_items_equal(fit0_.errs, fit1_.errs)


def test_optimal_distribution_normal():
    optimal = st.optimal_distribution(NORMAL)
    nt.ok_(optimal.type == 'norm')


def test_optimal_distribution_exponential():
    optimal = st.optimal_distribution(EXPON)
    nt.ok_(optimal.type == 'expon')


def test_optimal_distribution_uniform():
    optimal = st.optimal_distribution(UNIFORM)
    nt.ok_(optimal.type == 'uniform')


def test_fit_results_dict_uniform():
    a = st.FitResults(params=[1, 2], errs=[3,4], type='uniform')
    d = st.fit_results_to_dict(a)
    nt.assert_equal(d['min'], 1)
    nt.assert_equal(d['max'], 3)
    nt.assert_equal(d['type'], 'uniform')

def test_fit_results_dict_uniform_min_max():
    a = st.FitResults(params=[1, 2], errs=[3,4], type='uniform')
    d = st.fit_results_to_dict(a, min_bound=-100, max_bound=100)
    nt.assert_equal(d['min'], 1)
    nt.assert_equal(d['max'], 3)
    nt.assert_equal(d['type'], 'uniform')


def test_fit_results_dict_normal():
    a = st.FitResults(params=[1, 2], errs=[3,4], type='norm')
    d = st.fit_results_to_dict(a)
    nt.assert_equal(d['mu'], 1)
    nt.assert_equal(d['sigma'], 2)
    nt.assert_equal(d['type'], 'normal')


def test_fit_results_dict_normal_min_max():
    a = st.FitResults(params=[1, 2], errs=[3,4], type='norm')
    d = st.fit_results_to_dict(a, min_bound=-100, max_bound=100)
    nt.assert_equal(d['mu'], 1)
    nt.assert_equal(d['sigma'], 2)
    nt.assert_equal(d['min'], -100)
    nt.assert_equal(d['max'], 100)
    nt.assert_equal(d['type'], 'normal')


def test_fit_results_dict_exponential():
    a = st.FitResults(params=[2, 2], errs=[3,4], type='expon')
    d = st.fit_results_to_dict(a)
    nt.assert_equal(d['lambda'], 1./2)
    nt.assert_equal(d['type'], 'exponential')


def test_fit_results_dict_exponential_min_max():
    a = st.FitResults(params=[2, 2], errs=[3,4], type='expon')
    d = st.fit_results_to_dict(a, min_bound=-100, max_bound=100)
    nt.assert_equal(d['lambda'], 1./2)
    nt.assert_equal(d['min'], -100)
    nt.assert_equal(d['max'], 100)
    nt.assert_equal(d['type'], 'exponential')