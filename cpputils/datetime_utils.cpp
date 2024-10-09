// Copyright (c) 2024 Semjon Geist.

/*
 *****************************************************************
 *                    Date Time Parsing Utils                    *
 *                                                               *
 * Author: Arash Partow (2006)                                   *
 * URL: http://www.partow.net/programming/datetime/index.html    *
 *                                                               *
 * Note:                                                         *
 * The following code has a dependency on the StrTk library.     *
 * URL: http://www.partow.net/programming/strtk/index.html       *
 *                                                               *
 * Copyright notice:                                             *
 * Free use of the Date Time Parsing Utils Library is permitted  *
 * under the guidelines and in accordance with the MIT License.  *
 * http://www.opensource.org/licenses/MIT                        *
 *                                                               *
 *****************************************************************
 */

#define strtk_no_tr1_or_boost
#include <datetime_utils.hpp>

namespace dt_utils {

bool valid_date00(const datetime& dt) {
  if ((dt.day < 1) || (dt.day > 31))
    return false;
  else if ((dt.month < 1) || (dt.month > 12))
    return false;
  else
    return true;
}

bool valid_date01(const datetime& dt) {
  if ((dt.day < 1) || (dt.day > 31))
    return false;
  else if ((dt.month < 1) || (dt.month > 12))
    return false;

  static const unsigned int days_in_month[] = {0,  31, 28, 31, 30, 31, 30,
                                               31, 31, 30, 31, 30, 31};

  if (dt.month == 2) {
    struct is_leap_year {
      static inline bool process(const unsigned int y) {
        return (0 == (y % 4)) && ((0 != (y % 100)) || (0 == (y % 400)));
      }
    };

    if (!is_leap_year::process(dt.year))
      return (dt.day <= days_in_month[dt.month]);
    else
      return (dt.day <= 29);
  } else {
    return (dt.day <= days_in_month[dt.month]);
  }
}

bool valid_time00(const datetime& dt) {
  if (dt.hour > 23)
    return false;
  else if (dt.minute > 59)
    return false;
  else if (dt.second > 59)
    return false;
  else if (dt.millisecond > 999)
    return false;
  else if (dt.microsecond > 99999)
    return false;
  else
    return true;
}

bool valid_datetime00(const datetime& dt) {
  return valid_date00(dt) && valid_time00(dt);
}

bool valid_datetime01(const datetime& dt) {
  return valid_date01(dt) && valid_time00(dt);
}

bool lessthan_datetime(const datetime& dt0, const datetime& dt1) {
  if (dt0.year < dt1.year)
    return true;
  else if (dt0.year > dt1.year)
    return false;
  else if (dt0.month < dt1.month)
    return true;
  else if (dt0.month > dt1.month)
    return false;
  else if (dt0.day < dt1.day)
    return true;
  else if (dt0.day > dt1.day)
    return false;
  else if (dt0.hour < dt1.hour)
    return true;
  else if (dt0.hour > dt1.hour)
    return false;
  else if (dt0.minute < dt1.minute)
    return true;
  else if (dt0.minute > dt1.minute)
    return false;
  else if (dt0.second < dt1.second)
    return true;
  else
    return false;
}

bool lessthan_date(const datetime& dt0, const datetime& dt1) {
  if (dt0.year < dt1.year)
    return true;
  else if (dt0.year > dt1.year)
    return false;
  else if (dt0.month < dt1.month)
    return true;
  else if (dt0.month > dt1.month)
    return false;
  else if (dt0.day < dt1.day)
    return true;
  else
    return false;
}

bool lessthan_time(const datetime& dt0, const datetime& dt1) {
  if (dt0.hour < dt1.hour)
    return true;
  else if (dt0.hour > dt1.hour)
    return false;
  else if (dt0.minute < dt1.minute)
    return true;
  else if (dt0.minute > dt1.minute)
    return false;
  else if (dt0.second < dt1.second)
    return true;
  else
    return false;
}

dt_format* create_datetime(const std::string& format, datetime* dt) {
  if (format == "YYYYMMDD")
    return new details::date_format00_proxy(*dt);
  else if (format == "YYYYDDMM")
    return new details::date_format01_proxy(*dt);
  else if (format == "YYYY/MM/DD")
    return new details::date_format02_proxy(*dt);
  else if (format == "YYYY/DD/MM")
    return new details::date_format03_proxy(*dt);
  else if (format == "DD/MM/YYYY")
    return new details::date_format04_proxy(*dt);
  else if (format == "MM/DD/YYYY")
    return new details::date_format05_proxy(*dt);
  else if (format == "YYYY-MM-DD")
    return new details::date_format06_proxy(*dt);
  else if (format == "YYYY-DD-MM")
    return new details::date_format07_proxy(*dt);
  else if (format == "DD-MM-YYYY")
    return new details::date_format08_proxy(*dt);
  else if (format == "MM-DD-YYYY")
    return new details::date_format09_proxy(*dt);
  else if (format == "DD.MM.YYYY")
    return new details::date_format10_proxy(*dt);
  else if (format == "MM.DD.YYYY")
    return new details::date_format11_proxy(*dt);
  else if (format == "DD-Mon-YY")
    return new details::date_format12_proxy(*dt);
  else if (format == "?D-Mon-YY")
    return new details::date_format13_proxy(*dt);
  else if (format == "DD-Mon-YYYY")
    return new details::date_format14_proxy(*dt);
  else if (format == "?D-Mon-YYYY")
    return new details::date_format15_proxy(*dt);
  else if (format == "HH:MM:SS.mss")
    return new details::time_format0_proxy(*dt);
  else if (format == "HH:MM:SS")
    return new details::time_format1_proxy(*dt);
  else if (format == "HH MM SS mss")
    return new details::time_format2_proxy(*dt);
  else if (format == "HH MM SS")
    return new details::time_format3_proxy(*dt);
  else if (format == "HH.MM.SS.mss")
    return new details::time_format4_proxy(*dt);
  else if (format == "HH.MM.SS")
    return new details::time_format5_proxy(*dt);
  else if (format == "HHMM")
    return new details::time_format6_proxy(*dt);
  else if (format == "HHMMSS")
    return new details::time_format7_proxy(*dt);
  else if (format == "HHMMSSmss")
    return new details::time_format8_proxy(*dt);
  else if (format == "HHMMSS")
    return new details::time_format9_proxy(*dt);
  else if (format == "HHMMSSmss")
    return new details::time_format10_proxy(*dt);
  else if (format == "HHMMSS")
    return new details::time_format11_proxy(*dt);
  else if (format == "HHMMSS")
    return new details::time_format12_proxy(*dt);
  else if (format == "YYYYMMDD HH:MM:SS.mss")
    return new details::datetime_format00_proxy(*dt);
  else if (format == "YYYY/MM/DD HH:MM:SS.mss")
    return new details::datetime_format01_proxy(*dt);
  else if (format == "DD/MM/YYYY HH:MM:SS.mss")
    return new details::datetime_format02_proxy(*dt);
  else if (format == "YYYYMMDD HH:MM:SS")
    return new details::datetime_format03_proxy(*dt);
  else if (format == "YYYY/MM/DD HH:MM:SS")
    return new details::datetime_format04_proxy(*dt);
  else if (format == "DD/MM/YYYY HH:MM:SS")
    return new details::datetime_format05_proxy(*dt);
  else if (format == "YYYY-MM-DD HH:MM:SS.mss")
    return new details::datetime_format06_proxy(*dt);
  else if (format == "DD-MM-YYYY HH:MM:SS.mss")
    return new details::datetime_format07_proxy(*dt);
  else if (format == "YYYY-MM-DD HH:MM:SS")
    return new details::datetime_format08_proxy(*dt);
  else if (format == "DD-MM-YYYY HH:MM:SS")
    return new details::datetime_format09_proxy(*dt);
  else if (format == "YYYY-MM-D*dtHH:MM:SS")
    return new details::datetime_format10_proxy(*dt);
  else if (format == "YYYY-MM-D*dtHH:MM:SS.mss")
    return new details::datetime_format11_proxy(*dt);
  else if (format == "YYYYMMD*dtHH:MM:SS")
    return new details::datetime_format12_proxy(*dt);
  else if (format == "YYYYMMD*dtHH:MM:SS.mss")
    return new details::datetime_format13_proxy(*dt);
  else if (format == "DD-MM-YYYYTHH:MM:SS.mss")
    return new details::datetime_format14_proxy(*dt);
  else if (format == "DD-MM-YYYYTHH:MM:SS")
    return new details::datetime_format15_proxy(*dt);
  else if (format == "YYYYMMD*dtHHMM")
    return new details::datetime_format16_proxy(*dt);
  else if (format == "YYYYMMD*dtHHMMSS")
    return new details::datetime_format17_proxy(*dt);
  else if (format == "YYYYMMD*dtHHMMSSMSS")
    return new details::datetime_format18_proxy(*dt);
  else if (format == "ISO8601-0")
    return new details::datetime_format19_proxy(*dt);
  else if (format == "ISO8601-1")
    return new details::datetime_format20_proxy(*dt);
  else if (format == "CommonLog")
    return new details::datetime_format21_proxy(*dt);
  else if (format == "RFC822")
    return new details::datetime_format22_proxy(*dt);
  else if (format == "YYYYMMDD HH:MM:SS.nss")
    return new details::datetime_format23_proxy(*dt);
  else if (format == "YYYY/MM/DD HH:MM:SS.nss")
    return new details::datetime_format24_proxy(*dt);
  else if (format == "DD/MM/YYYY HH:MM:SS.nss")
    return new details::datetime_format25_proxy(*dt);
  else if (format == "YYYY-MM-DD HH:MM:SS.nss")
    return new details::datetime_format26_proxy(*dt);
  else if (format == "DD-MM-YYYY HH:MM:SS.nss")
    return new details::datetime_format27_proxy(*dt);
  else if (format == "YYYY-MM-D*dtHH:MM:SS.nss")
    return new details::datetime_format28_proxy(*dt);
  else if (format == "YYYYMMD*dtHH:MM:SS.nss")
    return new details::datetime_format29_proxy(*dt);
  else if (format == "DD-MM-YYYYTHH:MM:SS.nss")
    return new details::datetime_format30_proxy(*dt);
  else if (format == "YYYYMMD*dtHHMMSSNSS")
    return new details::datetime_format31_proxy(*dt);
  else if (format == "ISO8601-3")
    return new details::datetime_format32_proxy(*dt);
  else if (format == "ISO8601-4")
    return new details::datetime_format33_proxy(*dt);
  else
    return reinterpret_cast<dt_format*>(0);
}
}  // namespace dt_utils
