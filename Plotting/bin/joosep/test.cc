#define BOOST_TEST_DYN_LINK
#define BOOST_TEST_MODULE Simple testcases
#include <boost/test/unit_test.hpp>
#include <boost/test/test_tools.hpp>
#include <vector>

#include "TTH/MEAnalysis/interface/MECombination.h"


BOOST_AUTO_TEST_CASE(simple_test) {
  BOOST_CHECK_EQUAL(perm_maps::get_n(12345, 1), 5);
  BOOST_CHECK_EQUAL(perm_maps::get_n(12345, 2), 4);
  BOOST_CHECK_EQUAL(perm_maps::get_n(12345, 3), 3);
  BOOST_CHECK_EQUAL(perm_maps::get_n(12345, 4), 2);
  BOOST_CHECK_EQUAL(perm_maps::get_n(12345, 5), 1);

  std::vector<int> ret = perm_maps::comb_as_vector(12345, 5);
  std::vector<int> v{1,2,3,4,5};

  BOOST_CHECK_EQUAL_COLLECTIONS(ret.begin(), ret.end(), v.begin(), v.end());
}