// Copyright (c) 2024 Semjon Geist.

//
// Created by sgeist on 09.02.24.
//

#ifndef CPPUTILS_EVAL_DATETIME_HPP_
#define CPPUTILS_EVAL_DATETIME_HPP_

#include <string_operations.hpp>

namespace string_operations {

// TODO(sgeist): Replace the datetime_utils with another library (e.g. boost)

#ifndef DOXYGEN_SHOULD_SKIP_THIS
dt_utils::datetime global_dt{};
dt_utils::date_format00 date_format00(global_dt);
dt_utils::date_format01 date_format01(global_dt);
dt_utils::date_format02 date_format02(global_dt);
dt_utils::date_format03 date_format03(global_dt);
dt_utils::date_format04 date_format04(global_dt);
dt_utils::date_format05 date_format05(global_dt);
dt_utils::date_format06 date_format06(global_dt);
dt_utils::date_format07 date_format07(global_dt);
dt_utils::date_format08 date_format08(global_dt);
dt_utils::date_format09 date_format09(global_dt);
dt_utils::date_format10 date_format10(global_dt);
dt_utils::date_format11 date_format11(global_dt);
dt_utils::date_format12 date_format12(global_dt);
dt_utils::date_format13 date_format13(global_dt);
dt_utils::date_format14 date_format14(global_dt);
dt_utils::date_format15 date_format15(global_dt);
dt_utils::datetime_format00 datetime_format00(global_dt);
dt_utils::datetime_format01 datetime_format01(global_dt);
dt_utils::datetime_format02 datetime_format02(global_dt);
dt_utils::datetime_format03 datetime_format03(global_dt);
dt_utils::datetime_format04 datetime_format04(global_dt);
dt_utils::datetime_format05 datetime_format05(global_dt);
dt_utils::datetime_format06 datetime_format06(global_dt);
dt_utils::datetime_format07 datetime_format07(global_dt);
dt_utils::datetime_format08 datetime_format08(global_dt);
dt_utils::datetime_format09 datetime_format09(global_dt);
dt_utils::datetime_format10 datetime_format10(global_dt);
dt_utils::datetime_format11 datetime_format11(global_dt);
dt_utils::datetime_format12 datetime_format12(global_dt);
dt_utils::datetime_format13 datetime_format13(global_dt);
dt_utils::datetime_format14 datetime_format14(global_dt);
dt_utils::datetime_format15 datetime_format15(global_dt);
dt_utils::datetime_format16 datetime_format16(global_dt);
dt_utils::datetime_format17 datetime_format17(global_dt);
dt_utils::datetime_format18 datetime_format18(global_dt);
dt_utils::datetime_format19 datetime_format19(global_dt);
dt_utils::datetime_format20 datetime_format20(global_dt);
dt_utils::datetime_format21 datetime_format21(global_dt);
dt_utils::datetime_format22 datetime_format22(global_dt);
dt_utils::datetime_format23 datetime_format23(global_dt);
dt_utils::datetime_format24 datetime_format24(global_dt);
dt_utils::datetime_format25 datetime_format25(global_dt);
dt_utils::datetime_format26 datetime_format26(global_dt);
dt_utils::datetime_format27 datetime_format27(global_dt);
dt_utils::datetime_format28 datetime_format28(global_dt);
dt_utils::datetime_format29 datetime_format29(global_dt);
dt_utils::datetime_format30 datetime_format30(global_dt);
dt_utils::datetime_format31 datetime_format31(global_dt);
dt_utils::datetime_format32 datetime_format32(global_dt);
dt_utils::datetime_format33 datetime_format33(global_dt);
dt_utils::time_format0 time_format0(global_dt);
dt_utils::time_format1 time_format1(global_dt);
dt_utils::time_format2 time_format2(global_dt);
dt_utils::time_format3 time_format3(global_dt);
dt_utils::time_format4 time_format4(global_dt);
dt_utils::time_format5 time_format5(global_dt);
dt_utils::time_format6 time_format6(global_dt);
dt_utils::time_format7 time_format7(global_dt);
dt_utils::time_format8 time_format8(global_dt);
dt_utils::time_format9 time_format9(global_dt);
dt_utils::time_format10 time_format10(global_dt);
dt_utils::time_format11 time_format11(global_dt);
dt_utils::time_format12 time_format12(global_dt);
#endif /* DOXYGEN_SHOULD_SKIP_THIS */

py::object get_global_datetime() {
  return py::module::import("datetime")
      .attr("datetime")(
          global_dt.year, global_dt.month, global_dt.day, global_dt.hour,
          global_dt.minute, global_dt.second,
          global_dt.microsecond ? global_dt.microsecond
                                : global_dt.millisecond * 1000,
          py::module::import("datetime")
              .attr("timezone")(py::module::import("datetime")
                                    .attr("timedelta")(0, global_dt.tzd * 60)));
}

py::object get_global_date() {
  return py::module::import("datetime")
      .attr("date")(global_dt.year, global_dt.month, global_dt.day);
}

py::object get_global_time() {
  return py::module::import("datetime")
      .attr("time")(
          global_dt.hour, global_dt.minute, global_dt.second,
          global_dt.microsecond ? global_dt.microsecond
                                : global_dt.millisecond * 1000,
          py::module::import("datetime")
              .attr("timezone")(py::module::import("datetime")
                                    .attr("timedelta")(0, global_dt.tzd * 60)));
}

py::object to_generic_datetime(const std::string &value) {
  global_dt.clear();
  try {
    if (strtk::string_to_type_converter(value, datetime_format00))
      return get_global_datetime();
    if (strtk::string_to_type_converter(value, datetime_format01))
      return get_global_datetime();
    if (strtk::string_to_type_converter(value, datetime_format02))
      return get_global_datetime();
    if (strtk::string_to_type_converter(value, datetime_format03))
      return get_global_datetime();
    if (strtk::string_to_type_converter(value, datetime_format04))
      return get_global_datetime();
    if (strtk::string_to_type_converter(value, datetime_format05))
      return get_global_datetime();
    if (strtk::string_to_type_converter(value, datetime_format06))
      return get_global_datetime();
    if (strtk::string_to_type_converter(value, datetime_format07))
      return get_global_datetime();
    if (strtk::string_to_type_converter(value, datetime_format08))
      return get_global_datetime();
    if (strtk::string_to_type_converter(value, datetime_format09))
      return get_global_datetime();
    if (strtk::string_to_type_converter(value, datetime_format10))
      return get_global_datetime();
    if (strtk::string_to_type_converter(value, datetime_format11))
      return get_global_datetime();
    if (strtk::string_to_type_converter(value, datetime_format12))
      return get_global_datetime();
    if (strtk::string_to_type_converter(value, datetime_format13))
      return get_global_datetime();
    if (strtk::string_to_type_converter(value, datetime_format14))
      return get_global_datetime();
    if (strtk::string_to_type_converter(value, datetime_format15))
      return get_global_datetime();
    if (strtk::string_to_type_converter(value, datetime_format16))
      return get_global_datetime();
    if (strtk::string_to_type_converter(value, datetime_format17))
      return get_global_datetime();
    if (strtk::string_to_type_converter(value, datetime_format18))
      return get_global_datetime();
    if (strtk::string_to_type_converter(value, datetime_format19))
      return get_global_datetime();
    if (strtk::string_to_type_converter(value, datetime_format20))
      return get_global_datetime();
    if (strtk::string_to_type_converter(value, datetime_format21))
      return get_global_datetime();
    if (strtk::string_to_type_converter(value, datetime_format22))
      return get_global_datetime();
    if (strtk::string_to_type_converter(value, datetime_format23))
      return get_global_datetime();
    if (strtk::string_to_type_converter(value, datetime_format24))
      return get_global_datetime();
    if (strtk::string_to_type_converter(value, datetime_format25))
      return get_global_datetime();
    if (strtk::string_to_type_converter(value, datetime_format26))
      return get_global_datetime();
    if (strtk::string_to_type_converter(value, datetime_format27))
      return get_global_datetime();
    if (strtk::string_to_type_converter(value, datetime_format28))
      return get_global_datetime();
    if (strtk::string_to_type_converter(value, datetime_format29))
      return get_global_datetime();
    if (strtk::string_to_type_converter(value, datetime_format30))
      return get_global_datetime();
    if (strtk::string_to_type_converter(value, datetime_format31))
      return get_global_datetime();
    if (strtk::string_to_type_converter(value, datetime_format32))
      return get_global_datetime();
    if (strtk::string_to_type_converter(value, datetime_format33))
      return get_global_datetime();
    if (strtk::string_to_type_converter(value, date_format00))
      return get_global_date();
    if (strtk::string_to_type_converter(value, date_format01))
      return get_global_date();
    if (strtk::string_to_type_converter(value, date_format02))
      return get_global_date();
    if (strtk::string_to_type_converter(value, date_format03))
      return get_global_date();
    if (strtk::string_to_type_converter(value, date_format04))
      return get_global_date();
    if (strtk::string_to_type_converter(value, date_format05))
      return get_global_date();
    if (strtk::string_to_type_converter(value, date_format06))
      return get_global_date();
    if (strtk::string_to_type_converter(value, date_format07))
      return get_global_date();
    if (strtk::string_to_type_converter(value, date_format08))
      return get_global_date();
    if (strtk::string_to_type_converter(value, date_format09))
      return get_global_date();
    if (strtk::string_to_type_converter(value, date_format10))
      return get_global_date();
    if (strtk::string_to_type_converter(value, date_format11))
      return get_global_date();
    if (strtk::string_to_type_converter(value, date_format12))
      return get_global_date();
    if (strtk::string_to_type_converter(value, date_format13))
      return get_global_date();
    if (strtk::string_to_type_converter(value, date_format14))
      return get_global_date();
    if (strtk::string_to_type_converter(value, date_format15))
      return get_global_date();
    if (strtk::string_to_type_converter(value, time_format0))
      return get_global_time();
    if (strtk::string_to_type_converter(value, time_format1))
      return get_global_time();
    if (strtk::string_to_type_converter(value, time_format2))
      return get_global_time();
    if (strtk::string_to_type_converter(value, time_format3))
      return get_global_time();
    if (strtk::string_to_type_converter(value, time_format4))
      return get_global_time();
    if (strtk::string_to_type_converter(value, time_format5))
      return get_global_time();
    if (strtk::string_to_type_converter(value, time_format6))
      return get_global_time();
    if (strtk::string_to_type_converter(value, time_format7))
      return get_global_time();
    if (strtk::string_to_type_converter(value, time_format8))
      return get_global_time();
    if (strtk::string_to_type_converter(value, time_format9))
      return get_global_time();
    if (strtk::string_to_type_converter(value, time_format10))
      return get_global_time();
    if (strtk::string_to_type_converter(value, time_format11))
      return get_global_time();
    if (strtk::string_to_type_converter(value, time_format12))
      return get_global_time();
  } catch (...) {
    return py::cast(value);
  }

  return py::cast(value);
}

/// This is a simple C++ function to cast strings into python datetime object
///
/// @param value string to cast
/// @returns python object (time, date, datetime, datetime_ms)
/// @note This function returns the same value as string when no datetime type
/// is detected
py::object eval_datetime(const std::string &value) {
  return to_generic_datetime(value);
}

}  // namespace string_operations

#endif  // CPPUTILS_BINDINGS_HPP_
