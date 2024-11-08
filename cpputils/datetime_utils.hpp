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

#ifndef CPPUTILS_DATETIME_UTILS_HPP_
#define CPPUTILS_DATETIME_UTILS_HPP_

#define strtk_no_tr1_or_boost
#include <iostream>
#include <string>
#include <strtk/strtk.hpp>

// clang-format off
// NOLINTFILE
namespace dt_utils
{
struct datetime
{
  unsigned short year;
  unsigned short month;
  unsigned short day;
  unsigned short hour;
  unsigned short minute;
  unsigned short second;
  unsigned short millisecond;
  unsigned microsecond;
  short tzd; //as minutes.

  void clear()
  {
    year        = 0;
    month       = 0;
    day         = 0;
    hour        = 0;
    minute      = 0;
    second      = 0;
    millisecond = 0;
    microsecond = 0;
    tzd         = 0;
  }
};

struct base_format
{
  explicit base_format(datetime& d) : dt(d) {}
  datetime& dt;
};

/* YYYYMMDD    */ struct date_format00 : public base_format { explicit date_format00(datetime& d) : base_format(d) {} };
/* YYYYDDMM    */ struct date_format01 : public base_format { explicit date_format01(datetime& d) : base_format(d) {} };
/* YYYY/MM/DD  */ struct date_format02 : public base_format { explicit date_format02(datetime& d) : base_format(d) {} };
/* YYYY/DD/MM  */ struct date_format03 : public base_format { explicit date_format03(datetime& d) : base_format(d) {} };
/* DD/MM/YYYY  */ struct date_format04 : public base_format { explicit date_format04(datetime& d) : base_format(d) {} };
/* MM/DD/YYYY  */ struct date_format05 : public base_format { explicit date_format05(datetime& d) : base_format(d) {} };
/* YYYY-MM-DD  */ struct date_format06 : public base_format { explicit date_format06(datetime& d) : base_format(d) {} };
/* YYYY-DD-MM  */ struct date_format07 : public base_format { explicit date_format07(datetime& d) : base_format(d) {} };
/* DD-MM-YYYY  */ struct date_format08 : public base_format { explicit date_format08(datetime& d) : base_format(d) {} };
/* MM-DD-YYYY  */ struct date_format09 : public base_format { explicit date_format09(datetime& d) : base_format(d) {} };
/* DD.MM.YYYY  */ struct date_format10 : public base_format { explicit date_format10(datetime& d) : base_format(d) {} };
/* MM.DD.YYYY  */ struct date_format11 : public base_format { explicit date_format11(datetime& d) : base_format(d) {} };
/* DD-Mon-YY   */ struct date_format12 : public base_format { explicit date_format12(datetime& d) : base_format(d) {} };
/* ?D-Mon-YY   */ struct date_format13 : public base_format { explicit date_format13(datetime& d) : base_format(d) {} };
/* DD-Mon-YYYY */ struct date_format14 : public base_format { explicit date_format14(datetime& d) : base_format(d) {} };
/* ?D-Mon-YYYY */ struct date_format15 : public base_format { explicit date_format15(datetime& d) : base_format(d) {} };

/* HH:MM:SS.mss */ struct time_format0 : public base_format { explicit time_format0(datetime& d) : base_format(d) {} };
/* HH:MM:SS     */ struct time_format1 : public base_format { explicit time_format1(datetime& d) : base_format(d) {} };
/* HH MM SS mss */ struct time_format2 : public base_format { explicit time_format2(datetime& d) : base_format(d) {} };
/* HH MM SS     */ struct time_format3 : public base_format { explicit time_format3(datetime& d) : base_format(d) {} };
/* HH.MM.SS.mss */ struct time_format4 : public base_format { explicit time_format4(datetime& d) : base_format(d) {} };
/* HH.MM.SS     */ struct time_format5 : public base_format { explicit time_format5(datetime& d) : base_format(d) {} };
/* HHMM         */ struct time_format6 : public base_format { explicit time_format6(datetime& d) : base_format(d) {} };
/* HHMMSS       */ struct time_format7 : public base_format { explicit time_format7(datetime& d) : base_format(d) {} };
/* HHMMSSmss    */ struct time_format8 : public base_format { explicit time_format8(datetime& d) : base_format(d) {} };
/* HH:MM:SS.mssTZD */ struct time_format9 : public base_format { explicit time_format9(datetime& d) : base_format(d) {} };
/* HH:MM:SSTZD     */ struct time_format10 : public base_format { explicit time_format10(datetime& d) : base_format(d) {} };
/* HH:MM:SS.mcssTZD */ struct time_format11 : public base_format { explicit time_format11(datetime& d) : base_format(d) {} };
/* HH:MM:SS.mcss */ struct time_format12 : public base_format { explicit time_format12(datetime& d) : base_format(d) {} };

/* YYYYMMDD HH:MM:SS.mss    */ struct datetime_format00 : public base_format { explicit datetime_format00(datetime& d) : base_format(d) {} };
/* YYYY/MM/DD HH:MM:SS.mss  */ struct datetime_format01 : public base_format { explicit datetime_format01(datetime& d) : base_format(d) {} };
/* DD/MM/YYYY HH:MM:SS.mss  */ struct datetime_format02 : public base_format { explicit datetime_format02(datetime& d) : base_format(d) {} };
/* YYYYMMDD HH:MM:SS        */ struct datetime_format03 : public base_format { explicit datetime_format03(datetime& d) : base_format(d) {} };
/* YYYY/MM/DD HH:MM:SS      */ struct datetime_format04 : public base_format { explicit datetime_format04(datetime& d) : base_format(d) {} };
/* DD/MM/YYYY HH:MM:SS      */ struct datetime_format05 : public base_format { explicit datetime_format05(datetime& d) : base_format(d) {} };
/* YYYY-MM-DD HH:MM:SS.mss  */ struct datetime_format06 : public base_format { explicit datetime_format06(datetime& d) : base_format(d) {} };
/* DD-MM-YYYY HH:MM:SS.mss  */ struct datetime_format07 : public base_format { explicit datetime_format07(datetime& d) : base_format(d) {} };
/* YYYY-MM-DD HH:MM:SS      */ struct datetime_format08 : public base_format { explicit datetime_format08(datetime& d) : base_format(d) {} };
/* DD-MM-YYYY HH:MM:SS      */ struct datetime_format09 : public base_format { explicit datetime_format09(datetime& d) : base_format(d) {} };
/* YYYY-MM-DDTHH:MM:SS      */ struct datetime_format10 : public base_format { explicit datetime_format10(datetime& d) : base_format(d) {} };
/* YYYY-MM-DDTHH:MM:SS.mss  */ struct datetime_format11 : public base_format { explicit datetime_format11(datetime& d) : base_format(d) {} };
/* YYYYMMDDTHH:MM:SS        */ struct datetime_format12 : public base_format { explicit datetime_format12(datetime& d) : base_format(d) {} };
/* YYYYMMDDTHH:MM:SS.mss    */ struct datetime_format13 : public base_format { explicit datetime_format13(datetime& d) : base_format(d) {} };
/* DD-MM-YYYYTHH:MM:SS.mss  */ struct datetime_format14 : public base_format { explicit datetime_format14(datetime& d) : base_format(d) {} };
/* DD-MM-YYYYTHH:MM:SS      */ struct datetime_format15 : public base_format { explicit datetime_format15(datetime& d) : base_format(d) {} };
/* YYYYMMDDTHHMM            */ struct datetime_format16 : public base_format { explicit datetime_format16(datetime& d) : base_format(d) {} };
/* YYYYMMDDTHHMMSS          */ struct datetime_format17 : public base_format { explicit datetime_format17(datetime& d) : base_format(d) {} };
/* YYYYMMDDTHHMMSSMSS       */ struct datetime_format18 : public base_format { explicit datetime_format18(datetime& d) : base_format(d) {} };
/* ISO8601 + py DateThh:mm:ssTZD */ struct datetime_format19 : public base_format { explicit datetime_format19(datetime& d) : base_format(d) {} };
/* ISO8601 + py DateThh:mmTZD    */ struct datetime_format20 : public base_format { explicit datetime_format20(datetime& d) : base_format(d) {} };
/* NCSA Common Log DateTime */ struct datetime_format21 : public base_format { explicit datetime_format21(datetime& d) : base_format(d) {} };
/* RFC-822 HTTP DateTime    */ struct datetime_format22 : public base_format { explicit datetime_format22(datetime& d) : base_format(d) {} };
/* YYYYMMDD HH:MM:SS.nss    */ struct datetime_format23 : public base_format { explicit datetime_format23(datetime& d) : base_format(d) {} };
/* YYYY/MM/DD HH:MM:SS.mcss  */ struct datetime_format24 : public base_format { explicit datetime_format24(datetime& d) : base_format(d) {} };
/* DD/MM/YYYY HH:MM:SS.mcss  */ struct datetime_format25 : public base_format { explicit datetime_format25(datetime& d) : base_format(d) {} };
/* YYYY-MM-DD HH:MM:SS.mss  */ struct datetime_format26 : public base_format { explicit datetime_format26(datetime& d) : base_format(d) {} };
/* DD-MM-YYYY HH:MM:SS.mss  */ struct datetime_format27 : public base_format { explicit datetime_format27(datetime& d) : base_format(d) {} };
/* YYYY-MM-DDTHH:MM:SS.mss  */ struct datetime_format28 : public base_format { explicit datetime_format28(datetime& d) : base_format(d) {} };
/* YYYYMMDDTHH:MM:SS.mcss    */ struct datetime_format29 : public base_format { explicit datetime_format29(datetime& d) : base_format(d) {} };
/* DD-MM-YYYYTHH:MM:SS.mcss  */ struct datetime_format30 : public base_format { explicit datetime_format30(datetime& d) : base_format(d) {} };
/* YYYYMMDDTHHMMSSNSS       */ struct datetime_format31 : public base_format { explicit datetime_format31(datetime& d) : base_format(d) {} };
/* ISO8601 DateThh:mm:ss.mssTZD  */ struct datetime_format32 : public base_format { explicit datetime_format32(datetime& d) : base_format(d) {} };
/* ISO8601 DateThh:mm:ss.mcssTZD  */ struct datetime_format33 : public base_format { explicit datetime_format33(datetime& d) : base_format(d) {} };

class dt_format
{
 public:

  virtual ~dt_format() {}

  virtual bool process(const char* begin, const char* end) = 0;
};

namespace details
{
template <typename InputIterator>
bool parse_YYYYMMDD(InputIterator begin, InputIterator end, datetime& dt)
{
  const std::size_t date_size = 8;
  unsigned int date;
  if (date_size != static_cast<std::size_t>(std::distance(begin,end)))
    return false;
  else if (!strtk::fast::all_digits_check<8>(begin))
    return false;
  strtk::fast::numeric_convert<8>(begin,date);
  if (date < 101)
    return false;
  dt.month = (date % 10000) / 100;
  if(dt.month>12) return false;
  dt.year  = date / 10000;
  dt.day   = date % 100;
  return true;
}

template <typename InputIterator>
bool parse_YYYYDDMM(InputIterator begin, InputIterator end, datetime& dt)
{
  const std::size_t date_size = 8;
  unsigned int date;
  if (date_size != static_cast<std::size_t>(std::distance(begin,end)))
    return false;
  else if (!strtk::fast::all_digits_check<8>(begin))
    return false;
  strtk::fast::numeric_convert<8>(begin,date);
  if (date < 101)
    return false;
  dt.month = date % 100;
  if(dt.month>12) return false;
  dt.year  = date / 10000;
  dt.day   = (date % 10000) / 100;
  return true;
}

template <typename InputIterator>
unsigned int dow3chr_to_index(const InputIterator dow)
{
  /* Sun: 1, Mon: 2, Tue: 3, Wed: 4, Thu: 5, Fri: 6, Sat: 7 */
  const unsigned int error = 0;
  switch (std::toupper(dow[0]))
  {
    case 'M' : return (std::toupper(dow[1]) == 'O' && std::toupper(dow[2]) == 'N') ?  2 : error;
    case 'W' : return (std::toupper(dow[1]) == 'E' && std::toupper(dow[2]) == 'D') ?  4 : error;
    case 'F' : return (std::toupper(dow[1]) == 'R' && std::toupper(dow[2]) == 'I') ?  6 : error;
    case 'T' :
    {
      char c0 = std::toupper(dow[1]);
      char c1 = std::toupper(dow[2]);
      if (('U' == c0) && (c1 == 'E'))
        return 3;
      else if (('H' == c0) && (c1 == 'U'))
        return 5;
      else
        return error;
    }
    case 'S' :
    {
      char c0 = std::toupper(dow[1]);
      char c1 = std::toupper(dow[2]);
      if (('A' == c0) && (c1 == 'T'))
        return 7;
      else if (('U' == c0) && (c1 == 'N'))
        return 1;
      else
        return error;
    }
  }
  return false;
}

template <typename InputIterator>
unsigned int month3chr_to_index(const InputIterator month)
{
  const unsigned int error = 0;
  switch (std::toupper(month[0]))
  {
    case 'F' : return (std::toupper(month[1]) == 'E' && std::toupper(month[2]) == 'B') ?  2 : error; //February
    case 'D' : return (std::toupper(month[1]) == 'E' && std::toupper(month[2]) == 'C') ? 12 : error; //December
    case 'N' : return (std::toupper(month[1]) == 'O' && std::toupper(month[2]) == 'V') ? 11 : error; //November
    case 'O' : return (std::toupper(month[1]) == 'C' && std::toupper(month[2]) == 'T') ? 10 : error; //October
    case 'S' : return (std::toupper(month[1]) == 'E' && std::toupper(month[2]) == 'P') ?  9 : error; //September
    case 'A' :
    {
      char c0 = std::toupper(month[1]);
      char c1 = std::toupper(month[2]);
      if (('P' == c0) && (c1 == 'R'))      //April
        return 4;
      else if (('U' == c0) && (c1 == 'G')) //August
        return 8;
      else
        return error;
    }

    case 'J' :
    {
      char c0 = std::toupper(month[1]);
      char c1 = std::toupper(month[2]);
      if (('A' == c0) && (c1 == 'N'))      //January
        return 1;
      else if (('U' == c0) && (c1 == 'L')) //July
        return 7;
      else if (('U' == c0) && (c1 == 'N')) //June
        return 6;
      else
        return error;
    }

    case 'M' :
    {
      char c0 = std::toupper(month[1]);
      char c1 = std::toupper(month[2]);
      if (('A' == c0) && (c1 == 'R'))      //March
        return 3;
      else if (('A' == c0) && (c1 == 'Y')) //May
        return 5;
      else
        return error;
    }

    default : return error;
  }
}

template <typename InputIterator>
bool tzd3chr_to_offset(const InputIterator tzd, short& offset_mins)
{
  if ('T' != std::toupper(tzd[2]))
    return false;
  else if ('D' == std::toupper(tzd[1]))
  {
    switch (std::toupper(tzd[0]))
    {
      case 'E' : offset_mins = -4; break;
      case 'C' : offset_mins = -5; break;
      case 'M' : offset_mins = -6; break;
      case 'P' : offset_mins = -7; break;
      default  : return false;
    }
  }
  else if ('S' == std::toupper(tzd[1]))
  {
    switch (std::toupper(tzd[0]))
    {
      case 'E' : offset_mins = -5; break;
      case 'C' : offset_mins = -6; break;
      case 'M' : offset_mins = -7; break;
      case 'P' : offset_mins = -8; break;
      default  : return false;
    }
  }
  else if (('G' == std::toupper(tzd[0])) && ('M' == std::toupper(tzd[1])))
    offset_mins = 0;
  else
    return false;
  offset_mins *= 60;
  return true;
}

template <typename InputIterator>
bool miltzd1chr_to_offset(const InputIterator tzd, short& offset_mins)
{
  switch (std::toupper(tzd[0]))
  {
    case 'A' : offset_mins = -1;  break;
    case 'M' : offset_mins = -12; break;
    case 'N' : offset_mins = +1;  break;
    case 'Y' : offset_mins = +12; break;
    default  : return false;
  }
  offset_mins *= 60;
  return true;
}

#define register_datetime_format_proxy(Type)            \
      struct Type##_proxy : public dt_format                  \
      {                                                       \
         Type##_proxy(datetime& dt)                           \
         : dtf_(dt)                                           \
         {}                                                   \
         Type dtf_;                                           \
         bool process(const char* b, const char* e)           \
         {                                                    \
            return strtk::string_to_type_converter(b,e,dtf_); \
         }                                                    \
      };                                                      \

register_datetime_format_proxy(date_format00)
register_datetime_format_proxy(date_format01)
register_datetime_format_proxy(date_format02)
register_datetime_format_proxy(date_format03)
register_datetime_format_proxy(date_format04)
register_datetime_format_proxy(date_format05)
register_datetime_format_proxy(date_format06)
register_datetime_format_proxy(date_format07)
register_datetime_format_proxy(date_format08)
register_datetime_format_proxy(date_format09)
register_datetime_format_proxy(date_format10)
register_datetime_format_proxy(date_format11)
register_datetime_format_proxy(date_format12)
register_datetime_format_proxy(date_format13)
register_datetime_format_proxy(date_format14)
register_datetime_format_proxy(date_format15)
register_datetime_format_proxy(time_format0)
register_datetime_format_proxy(time_format1)
register_datetime_format_proxy(time_format2)
register_datetime_format_proxy(time_format3)
register_datetime_format_proxy(time_format4)
register_datetime_format_proxy(time_format5)
register_datetime_format_proxy(time_format6)
register_datetime_format_proxy(time_format7)
register_datetime_format_proxy(time_format8)
register_datetime_format_proxy(time_format9)
register_datetime_format_proxy(time_format10)
register_datetime_format_proxy(time_format11)
register_datetime_format_proxy(time_format12)
register_datetime_format_proxy(datetime_format00)
register_datetime_format_proxy(datetime_format01)
register_datetime_format_proxy(datetime_format02)
register_datetime_format_proxy(datetime_format03)
register_datetime_format_proxy(datetime_format04)
register_datetime_format_proxy(datetime_format05)
register_datetime_format_proxy(datetime_format06)
register_datetime_format_proxy(datetime_format07)
register_datetime_format_proxy(datetime_format08)
register_datetime_format_proxy(datetime_format09)
register_datetime_format_proxy(datetime_format10)
register_datetime_format_proxy(datetime_format11)
register_datetime_format_proxy(datetime_format12)
register_datetime_format_proxy(datetime_format13)
register_datetime_format_proxy(datetime_format14)
register_datetime_format_proxy(datetime_format15)
register_datetime_format_proxy(datetime_format16)
register_datetime_format_proxy(datetime_format17)
register_datetime_format_proxy(datetime_format18)
register_datetime_format_proxy(datetime_format19)
register_datetime_format_proxy(datetime_format20)
register_datetime_format_proxy(datetime_format21)
register_datetime_format_proxy(datetime_format22)
register_datetime_format_proxy(datetime_format23)
register_datetime_format_proxy(datetime_format24)
register_datetime_format_proxy(datetime_format25)
register_datetime_format_proxy(datetime_format26)
register_datetime_format_proxy(datetime_format27)
register_datetime_format_proxy(datetime_format28)
register_datetime_format_proxy(datetime_format29)
register_datetime_format_proxy(datetime_format30)
register_datetime_format_proxy(datetime_format31)
register_datetime_format_proxy(datetime_format32)
register_datetime_format_proxy(datetime_format33)
}

bool valid_date00(const datetime& dt);

bool valid_date01(const datetime& dt);

bool valid_time00(const datetime& dt);

bool valid_datetime00(const datetime& dt);

bool valid_datetime01(const datetime& dt);

bool lessthan_datetime(const datetime& dt0, const datetime& dt1);

bool lessthan_date(const datetime& dt0, const datetime& dt1);

bool lessthan_time(const datetime& dt0, const datetime& dt1);

dt_format* create_datetime(const std::string& format, datetime* dt);
}


strtk_string_to_type_begin(dt_utils::dt_format*)
  // cppcheck-suppress syntaxError
  return t->process(begin,end);
strtk_string_to_type_end()

strtk_string_to_type_begin(dt_utils::date_format00)
  if (8 != std::distance(begin,end))
    return false;
  else
    return dt_utils::details::parse_YYYYMMDD(begin,begin + 8,t.dt);
strtk_string_to_type_end()

strtk_string_to_type_begin(dt_utils::date_format01)
  if (8 != std::distance(begin,end))
    return false;
  else
    return dt_utils::details::parse_YYYYDDMM(begin,begin + 8,t.dt);
strtk_string_to_type_end()

strtk_string_to_type_begin(dt_utils::date_format02)
  if (10 != std::distance(begin,end))
    return false;
  else if (('/' != *(begin + 4)) || ('/' != *(begin + 7)))
    return false;
  else if (
      !strtk::fast::all_digits_check<4>(begin + 0) ||
          !strtk::fast::all_digits_check<2>(begin + 5) ||
          !strtk::fast::all_digits_check<2>(begin + 8)
      )
    return false;
  strtk::fast::numeric_convert<4>(begin + 0,t.dt.year );
  strtk::fast::numeric_convert<2>(begin + 5,t.dt.month);
  strtk::fast::numeric_convert<2>(begin + 8,t.dt.day  );
  return true;
strtk_string_to_type_end()

strtk_string_to_type_begin(dt_utils::date_format03)
  if (10 != std::distance(begin,end))
    return false;
  else if (('/' != *(begin + 4)) || ('/' != *(begin + 7)))
    return false;
  else if (
      !strtk::fast::all_digits_check<4>(begin + 0) ||
          !strtk::fast::all_digits_check<2>(begin + 5) ||
          !strtk::fast::all_digits_check<2>(begin + 8)
      )
    return false;
  strtk::fast::numeric_convert<4>(begin + 0,t.dt.year );
  strtk::fast::numeric_convert<2>(begin + 5,t.dt.day  );
  strtk::fast::numeric_convert<2>(begin + 8,t.dt.month);
  return true;
strtk_string_to_type_end()

strtk_string_to_type_begin(dt_utils::date_format04)
  if (10 != std::distance(begin,end))
    return false;
  else if (('/' != *(begin + 2)) || ('/' != *(begin + 5)))
    return false;
  else if (
      !strtk::fast::all_digits_check<2>(begin + 0) ||
          !strtk::fast::all_digits_check<2>(begin + 3) ||
          !strtk::fast::all_digits_check<4>(begin + 6)
      )
    return false;
  strtk::fast::numeric_convert<2>(begin + 0,t.dt.day  );
  strtk::fast::numeric_convert<2>(begin + 3,t.dt.month);
  strtk::fast::numeric_convert<4>(begin + 6,t.dt.year );
  return true;
strtk_string_to_type_end()

strtk_string_to_type_begin(dt_utils::date_format05)
  if (10 != std::distance(begin,end))
    return false;
  else if (('/' != *(begin + 2)) || ('/' != *(begin + 5)))
    return false;
  else if (
      !strtk::fast::all_digits_check<2>(begin + 0) ||
          !strtk::fast::all_digits_check<2>(begin + 3) ||
          !strtk::fast::all_digits_check<4>(begin + 6)
      )
    return false;
  strtk::fast::numeric_convert<2>(begin + 0,t.dt.month);
  strtk::fast::numeric_convert<2>(begin + 3,t.dt.day  );
  strtk::fast::numeric_convert<4>(begin + 6,t.dt.year );
  return true;
strtk_string_to_type_end()

strtk_string_to_type_begin(dt_utils::date_format06)
  if (10 != std::distance(begin,end))
    return false;
  else if (('-' != *(begin + 4)) || ('-' != *(begin + 7)))
    return false;
  else if (
      !strtk::fast::all_digits_check<4>(begin + 0) ||
          !strtk::fast::all_digits_check<2>(begin + 5) ||
          !strtk::fast::all_digits_check<2>(begin + 8)
      )
    return false;
  strtk::fast::numeric_convert<4>(begin + 0,t.dt.year );
  strtk::fast::numeric_convert<2>(begin + 5,t.dt.month);
  strtk::fast::numeric_convert<2>(begin + 8,t.dt.day  );
  return true;
strtk_string_to_type_end()

strtk_string_to_type_begin(dt_utils::date_format07)
  if (10 != std::distance(begin,end))
    return false;
  else if (('-' != *(begin + 4)) || ('-' != *(begin + 7)))
    return false;
  else if (
      !strtk::fast::all_digits_check<4>(begin + 0) ||
          !strtk::fast::all_digits_check<2>(begin + 5) ||
          !strtk::fast::all_digits_check<2>(begin + 8)
      )
    return false;
  strtk::fast::numeric_convert<4>(begin + 0,t.dt.year );
  strtk::fast::numeric_convert<2>(begin + 5,t.dt.day  );
  strtk::fast::numeric_convert<2>(begin + 8,t.dt.month);
  return true;
strtk_string_to_type_end()

strtk_string_to_type_begin(dt_utils::date_format08)
  if (10 != std::distance(begin,end))
    return false;
  else if (('-' != *(begin + 2)) || ('-' != *(begin + 5)))
    return false;
  else if (
      !strtk::fast::all_digits_check<2>(begin + 0) ||
          !strtk::fast::all_digits_check<2>(begin + 3) ||
          !strtk::fast::all_digits_check<4>(begin + 6)
      )
    return false;
  strtk::fast::numeric_convert<2>(begin + 0,t.dt.day  );
  strtk::fast::numeric_convert<2>(begin + 3,t.dt.month);
  strtk::fast::numeric_convert<4>(begin + 6,t.dt.year );
  return true;
strtk_string_to_type_end()

strtk_string_to_type_begin(dt_utils::date_format09)
  if (10 != std::distance(begin,end))
    return false;
  else if (('-' != *(begin + 2)) || ('-' != *(begin + 5)))
    return false;
  else if (
      !strtk::fast::all_digits_check<2>(begin + 0) ||
          !strtk::fast::all_digits_check<2>(begin + 3) ||
          !strtk::fast::all_digits_check<4>(begin + 6)
      )
    return false;
  strtk::fast::numeric_convert<2>(begin + 0,t.dt.month);
  strtk::fast::numeric_convert<2>(begin + 3,t.dt.day  );
  strtk::fast::numeric_convert<4>(begin + 6,t.dt.year );
  return true;
strtk_string_to_type_end()

strtk_string_to_type_begin(dt_utils::date_format10)
  if (10 != std::distance(begin,end))
    return false;
  else if (('.' != *(begin + 2)) || ('.' != *(begin + 5)))
    return false;
  else if (
      !strtk::fast::all_digits_check<2>(begin + 0) ||
          !strtk::fast::all_digits_check<2>(begin + 3) ||
          !strtk::fast::all_digits_check<4>(begin + 6)
      )
    return false;
  strtk::fast::numeric_convert<2>(begin + 0,t.dt.day  );
  strtk::fast::numeric_convert<2>(begin + 3,t.dt.month);
  strtk::fast::numeric_convert<4>(begin + 6,t.dt.year );
  return true;
strtk_string_to_type_end()

strtk_string_to_type_begin(dt_utils::date_format11)
  if (10 != std::distance(begin,end))
    return false;
  else if (('.' != *(begin + 2)) || ('.' != *(begin + 5)))
    return false;
  else if (
      !strtk::fast::all_digits_check<2>(begin + 0) ||
          !strtk::fast::all_digits_check<2>(begin + 3) ||
          !strtk::fast::all_digits_check<4>(begin + 6)
      )
    return false;
  strtk::fast::numeric_convert<2>(begin + 0,t.dt.month);
  strtk::fast::numeric_convert<2>(begin + 3,t.dt.day  );
  strtk::fast::numeric_convert<4>(begin + 6,t.dt.year );
  return true;
strtk_string_to_type_end()

strtk_string_to_type_begin(dt_utils::date_format12)
  if (9 != std::distance(begin,end))
    return false;
  else if (('-' != *(begin + 2)) || ('-' != *(begin + 6)))
    return false;
  else if (
      !strtk::fast::all_digits_check<2>(begin + 0) ||
          !strtk::fast::all_digits_check<2>(begin + 7)
      )
    return false;
  strtk::fast::numeric_convert<2>(begin + 0,t.dt.day );
  strtk::fast::numeric_convert<2>(begin + 7,t.dt.year);
  return (0 != (t.dt.month = dt_utils::details::month3chr_to_index(begin + 3)));
strtk_string_to_type_end()

strtk_string_to_type_begin(dt_utils::date_format13)
  const std::size_t length = std::distance(begin,end);
  if (9 == length)
  {
    if (('-' != *(begin + 2)) || ('-' != *(begin + 6)))
      return false;
    else if (
        !strtk::fast::all_digits_check<2>(begin + 0) ||
            !strtk::fast::all_digits_check<2>(begin + 7)
        )
      return false;
    strtk::fast::numeric_convert<2>(begin + 0,t.dt.day );
    strtk::fast::numeric_convert<2>(begin + 7,t.dt.year);
    return (0 != (t.dt.month = dt_utils::details::month3chr_to_index(begin + 3)));
  }
  else if (8 == length)
  {
    if (('-' != *(begin + 1)) || ('-' != *(begin + 5)))
      return false;
    else if (
        !strtk::fast::all_digits_check<1>(begin + 0) ||
            !strtk::fast::all_digits_check<2>(begin + 6)
        )
      return false;
    strtk::fast::numeric_convert<1>(begin + 0,t.dt.day );
    strtk::fast::numeric_convert<2>(begin + 6,t.dt.year);
    return (0 != (t.dt.month = dt_utils::details::month3chr_to_index(begin + 2)));
  }
  else
    return false;
strtk_string_to_type_end()

strtk_string_to_type_begin(dt_utils::date_format14)
  if (11 != std::distance(begin,end))
    return false;
  else if (('-' != *(begin + 2)) || ('-' != *(begin + 6)))
    return false;
  else if (
      !strtk::fast::all_digits_check<2>(begin + 0) ||
          !strtk::fast::all_digits_check<4>(begin + 7)
      )
    return false;
  strtk::fast::numeric_convert<2>(begin + 0,t.dt.day );
  strtk::fast::numeric_convert<4>(begin + 7,t.dt.year);
  return (0 != (t.dt.month = dt_utils::details::month3chr_to_index(begin + 3)));
strtk_string_to_type_end()

strtk_string_to_type_begin(dt_utils::date_format15)
  const std::size_t length = std::distance(begin,end);
  if (11 == length)
  {
    if (('-' != *(begin + 2)) || ('-' != *(begin + 6)))
      return false;
    else if (
        !strtk::fast::all_digits_check<2>(begin + 0) ||
            !strtk::fast::all_digits_check<4>(begin + 7)
        )
      return false;
    strtk::fast::numeric_convert<2>(begin + 0,t.dt.day );
    strtk::fast::numeric_convert<4>(begin + 7,t.dt.year);
    return (0 != (t.dt.month = dt_utils::details::month3chr_to_index(begin + 3)));
  }
  else if (10 == length)
  {
    if (('-' != *(begin + 1)) || ('-' != *(begin + 5)))
      return false;
    else if (
        !strtk::fast::all_digits_check<1>(begin + 0) ||
            !strtk::fast::all_digits_check<4>(begin + 6)
        )
      return false;
    strtk::fast::numeric_convert<1>(begin + 0,t.dt.day );
    strtk::fast::numeric_convert<4>(begin + 6,t.dt.year);
    return (0 != (t.dt.month = dt_utils::details::month3chr_to_index(begin + 2)));
  }
  else
    return false;
strtk_string_to_type_end()

strtk_string_to_type_begin(dt_utils::time_format0)
  if (12 != std::distance(begin,end))
    return false;
  else if (
      (':' != *(begin + 2)) ||
          (':' != *(begin + 5)) ||
          ('.' != *(begin + 8))
      )
    return false;
  else if (
      !strtk::fast::all_digits_check<2>(begin + 0) ||
          !strtk::fast::all_digits_check<2>(begin + 3) ||
          !strtk::fast::all_digits_check<2>(begin + 6) ||
          !strtk::fast::all_digits_check<3>(begin + 9)
      )
    return false;
  strtk::fast::numeric_convert<2>(begin + 0,t.dt.hour       );
  strtk::fast::numeric_convert<2>(begin + 3,t.dt.minute     );
  strtk::fast::numeric_convert<2>(begin + 6,t.dt.second     );
  strtk::fast::numeric_convert<3>(begin + 9,t.dt.millisecond);
  return true;
strtk_string_to_type_end()

strtk_string_to_type_begin(dt_utils::time_format1)
  if (8 != std::distance(begin,end))
    return false;
  else if ((':' != *(begin + 2)) || (':' != *(begin + 5)))
    return false;
  else if (
      !strtk::fast::all_digits_check<2>(begin + 0) ||
          !strtk::fast::all_digits_check<2>(begin + 3) ||
          !strtk::fast::all_digits_check<2>(begin + 6)
      )
    return false;
  strtk::fast::numeric_convert<2>(begin + 0,t.dt.hour  );
  strtk::fast::numeric_convert<2>(begin + 3,t.dt.minute);
  strtk::fast::numeric_convert<2>(begin + 6,t.dt.second);
  return true;
strtk_string_to_type_end()

strtk_string_to_type_begin(dt_utils::time_format2)
  if (12 != std::distance(begin,end))
    return false;
  else if (
      (' ' != *(begin + 2)) ||
          (' ' != *(begin + 5)) ||
          (' ' != *(begin + 8))
      )
    return false;
  else if (
      !strtk::fast::all_digits_check<2>(begin + 0) ||
          !strtk::fast::all_digits_check<2>(begin + 3) ||
          !strtk::fast::all_digits_check<2>(begin + 6) ||
          !strtk::fast::all_digits_check<3>(begin + 9)
      )
    return false;
  strtk::fast::numeric_convert<2>(begin + 0,t.dt.hour       );
  strtk::fast::numeric_convert<2>(begin + 3,t.dt.minute     );
  strtk::fast::numeric_convert<2>(begin + 6,t.dt.second     );
  strtk::fast::numeric_convert<3>(begin + 9,t.dt.millisecond);
  return true;
strtk_string_to_type_end()

strtk_string_to_type_begin(dt_utils::time_format3)
  if (8 != std::distance(begin,end))
    return false;
  else if ((' ' != *(begin + 2)) || (' ' != *(begin + 5)))
    return false;
  else if (
      !strtk::fast::all_digits_check<2>(begin + 0) ||
          !strtk::fast::all_digits_check<2>(begin + 3) ||
          !strtk::fast::all_digits_check<2>(begin + 6)
      )
    return false;
  strtk::fast::numeric_convert<2>(begin + 0,t.dt.hour  );
  strtk::fast::numeric_convert<2>(begin + 3,t.dt.minute);
  strtk::fast::numeric_convert<2>(begin + 6,t.dt.second);
  return true;
strtk_string_to_type_end()

strtk_string_to_type_begin(dt_utils::time_format4)
  if (12 != std::distance(begin,end))
    return false;
  else if (
      ('.' != *(begin + 2)) ||
          ('.' != *(begin + 5)) ||
          ('.' != *(begin + 8))
      )
    return false;
  else if (
      !strtk::fast::all_digits_check<2>(begin + 0) ||
          !strtk::fast::all_digits_check<2>(begin + 3) ||
          !strtk::fast::all_digits_check<2>(begin + 6) ||
          !strtk::fast::all_digits_check<3>(begin + 9)
      )
    return false;
  strtk::fast::numeric_convert<2>(begin + 0,t.dt.hour       );
  strtk::fast::numeric_convert<2>(begin + 3,t.dt.minute     );
  strtk::fast::numeric_convert<2>(begin + 6,t.dt.second     );
  strtk::fast::numeric_convert<3>(begin + 9,t.dt.millisecond);
  return true;
strtk_string_to_type_end()

strtk_string_to_type_begin(dt_utils::time_format5)
  if (8 != std::distance(begin,end))
    return false;
  else if (('.' != *(begin + 2)) || ('.' != *(begin + 5)))
    return false;
  else if (
      !strtk::fast::all_digits_check<2>(begin + 0) ||
          !strtk::fast::all_digits_check<2>(begin + 3) ||
          !strtk::fast::all_digits_check<2>(begin + 6)
      )
    return false;
  strtk::fast::numeric_convert<2>(begin + 0,t.dt.hour  );
  strtk::fast::numeric_convert<2>(begin + 3,t.dt.minute);
  strtk::fast::numeric_convert<2>(begin + 6,t.dt.second);
  return true;
strtk_string_to_type_end()

strtk_string_to_type_begin(dt_utils::time_format6)
  if (4 != std::distance(begin,end))
    return false;
  else if (
      !strtk::fast::all_digits_check<2>(begin + 0) ||
          !strtk::fast::all_digits_check<2>(begin + 2)
      )
    return false;
  strtk::fast::numeric_convert<2>(begin + 0,t.dt.hour  );
  strtk::fast::numeric_convert<2>(begin + 2,t.dt.minute);
  return true;
strtk_string_to_type_end()

strtk_string_to_type_begin(dt_utils::time_format7)
  if (6 != std::distance(begin,end))
    return false;
  else if (
      !strtk::fast::all_digits_check<2>(begin + 0) ||
          !strtk::fast::all_digits_check<2>(begin + 2) ||
          !strtk::fast::all_digits_check<2>(begin + 4)
      )
    return false;
  strtk::fast::numeric_convert<2>(begin + 0,t.dt.hour  );
  strtk::fast::numeric_convert<2>(begin + 2,t.dt.minute);
  strtk::fast::numeric_convert<2>(begin + 4,t.dt.second);
  return true;
strtk_string_to_type_end()

strtk_string_to_type_begin(dt_utils::time_format8)
  if (9 != std::distance(begin,end))
    return false;
  else if (
      !strtk::fast::all_digits_check<2>(begin + 0) ||
          !strtk::fast::all_digits_check<2>(begin + 2) ||
          !strtk::fast::all_digits_check<2>(begin + 4) ||
          !strtk::fast::all_digits_check<3>(begin + 6)
      )
    return false;
  strtk::fast::numeric_convert<2>(begin + 0,t.dt.hour  );
  strtk::fast::numeric_convert<2>(begin + 2,t.dt.minute);
  strtk::fast::numeric_convert<2>(begin + 4,t.dt.second);
  strtk::fast::numeric_convert<3>(begin + 6,t.dt.millisecond);
  return true;
strtk_string_to_type_end()

strtk_string_to_type_begin(dt_utils::time_format9)
  if (18 != std::distance(begin,end))
    return false;
  else if (
      (':' != *(begin + 2)) ||
          (':' != *(begin + 5)) ||
          ('.' != *(begin + 8)) ||
          (('-' != *(begin + 12)) && ('+' != *(begin + 12))) ||
          (':' != *(begin + 15))
      )
    return false;
  else if (
      !strtk::fast::all_digits_check<2>(begin + 0) ||
          !strtk::fast::all_digits_check<2>(begin + 3) ||
          !strtk::fast::all_digits_check<2>(begin + 6) ||
          !strtk::fast::all_digits_check<3>(begin + 9) ||
          !strtk::fast::all_digits_check<2>(begin + 13)||
          !strtk::fast::all_digits_check<2>(begin + 16)
      )
    return false;
  strtk::fast::numeric_convert<2>(begin + 0,t.dt.hour       );
  strtk::fast::numeric_convert<2>(begin + 3,t.dt.minute     );
  strtk::fast::numeric_convert<2>(begin + 6,t.dt.second     );
  strtk::fast::numeric_convert<3>(begin + 9,t.dt.millisecond);
  unsigned short tzd_hh;
  unsigned short tzd_mm;
  strtk::fast::numeric_convert<2>(begin + 13, tzd_hh);
  strtk::fast::numeric_convert<2>(begin + 16, tzd_mm);
  t.dt.tzd = ((tzd_hh * 60) + tzd_mm) * (('-' == *(begin + 12)) ? -1 : 1);
  return true;
strtk_string_to_type_end()


strtk_string_to_type_begin(dt_utils::time_format10)
  if (14 != std::distance(begin,end))
    return false;
  else if (
      (':' != *(begin + 2)) ||
          (':' != *(begin + 5)) ||
          (('-' != *(begin + 8)) && ('+' != *(begin + 8))) ||
          (':' != *(begin + 11))
      )
    return false;
  else if (
      !strtk::fast::all_digits_check<2>(begin + 0) ||
          !strtk::fast::all_digits_check<2>(begin + 3) ||
          !strtk::fast::all_digits_check<2>(begin + 6) ||
          !strtk::fast::all_digits_check<2>(begin + 9)||
          !strtk::fast::all_digits_check<2>(begin + 12)
      )
    return false;
  strtk::fast::numeric_convert<2>(begin + 0,t.dt.hour  );
  strtk::fast::numeric_convert<2>(begin + 3,t.dt.minute);
  strtk::fast::numeric_convert<2>(begin + 6,t.dt.second);
  unsigned short tzd_hh;
  unsigned short tzd_mm;
  strtk::fast::numeric_convert<2>(begin + 9, tzd_hh);
  strtk::fast::numeric_convert<2>(begin + 12, tzd_mm);
  t.dt.tzd = ((tzd_hh * 60) + tzd_mm) * (('-' == *(begin + 8)) ? -1 : 1);
  return true;
strtk_string_to_type_end()


strtk_string_to_type_begin(dt_utils::time_format11)
  if (21 != std::distance(begin,end))
    return false;
  else if (
      (':' != *(begin + 2)) ||
          (':' != *(begin + 5)) ||
          ('.' != *(begin + 8)) ||
          (('-' != *(begin + 15)) && ('+' != *(begin + 15))) ||
          (':' != *(begin + 18))
      )
    return false;
  else if (
      !strtk::fast::all_digits_check<2>(begin + 0) ||
          !strtk::fast::all_digits_check<2>(begin + 3) ||
          !strtk::fast::all_digits_check<2>(begin + 6) ||
          !strtk::fast::all_digits_check<6>(begin + 9) ||
          !strtk::fast::all_digits_check<2>(begin + 16)||
          !strtk::fast::all_digits_check<2>(begin + 19)
      )
    return false;
  strtk::fast::numeric_convert<2>(begin + 0,t.dt.hour       );
  strtk::fast::numeric_convert<2>(begin + 3,t.dt.minute     );
  strtk::fast::numeric_convert<2>(begin + 6,t.dt.second     );
  strtk::fast::numeric_convert<6>(begin + 9,t.dt.microsecond );
  unsigned short tzd_hh;
  unsigned short tzd_mm;
  strtk::fast::numeric_convert<2>(begin + 16, tzd_hh);
  strtk::fast::numeric_convert<2>(begin + 19, tzd_mm);
  t.dt.tzd = ((tzd_hh * 60) + tzd_mm) * (('-' == *(begin + 15)) ? -1 : 1);
  return true;
strtk_string_to_type_end()

strtk_string_to_type_begin(dt_utils::time_format12)
  if (15 != std::distance(begin,end))
    return false;
  else if (
      (':' != *(begin + 2)) ||
          (':' != *(begin + 5)) ||
          ('.' != *(begin + 8))
      )
    return false;
  else if (
      !strtk::fast::all_digits_check<2>(begin + 0) ||
          !strtk::fast::all_digits_check<2>(begin + 3) ||
          !strtk::fast::all_digits_check<2>(begin + 6) ||
          !strtk::fast::all_digits_check<6>(begin + 9)
      )
    return false;
  strtk::fast::numeric_convert<2>(begin + 0,t.dt.hour       );
  strtk::fast::numeric_convert<2>(begin + 3,t.dt.minute     );
  strtk::fast::numeric_convert<2>(begin + 6,t.dt.second     );
  strtk::fast::numeric_convert<6>(begin + 9,t.dt.microsecond);
  return true;
strtk_string_to_type_end()

strtk_string_to_type_begin(dt_utils::datetime_format00)
  if (21 != std::distance(begin,end))
    return false;
  else if (!dt_utils::details::parse_YYYYMMDD(begin,begin + 8,t.dt))
    return false;
  else if (
      (' ' != *(begin +  8)) || (':' != *(begin + 11)) ||
          (':' != *(begin + 14)) || ('.' != *(begin + 17))
      )
    return false;
  else if (
      !strtk::fast::all_digits_check<2>(begin +  9) ||
          !strtk::fast::all_digits_check<2>(begin + 12) ||
          !strtk::fast::all_digits_check<2>(begin + 15) ||
          !strtk::fast::all_digits_check<3>(begin + 18)
      )
    return false;
  strtk::fast::numeric_convert<2>(begin +  9,t.dt.hour       );
  strtk::fast::numeric_convert<2>(begin + 12,t.dt.minute     );
  strtk::fast::numeric_convert<2>(begin + 15,t.dt.second     );
  strtk::fast::numeric_convert<3>(begin + 18,t.dt.millisecond);
  return true;
strtk_string_to_type_end()

strtk_string_to_type_begin(dt_utils::datetime_format23)
  if (24 != std::distance(begin,end))
    return false;
  else if (!dt_utils::details::parse_YYYYMMDD(begin,begin + 8,t.dt))
    return false;
  else if (
      (' ' != *(begin +  8)) || (':' != *(begin + 11)) ||
          (':' != *(begin + 14)) || ('.' != *(begin + 17))
      )
    return false;
  else if (
      !strtk::fast::all_digits_check<2>(begin +  9) ||
          !strtk::fast::all_digits_check<2>(begin + 12) ||
          !strtk::fast::all_digits_check<2>(begin + 15) ||
          !strtk::fast::all_digits_check<6>(begin + 18)
      )
    return false;
  strtk::fast::numeric_convert<2>(begin +  9,t.dt.hour       );
  strtk::fast::numeric_convert<2>(begin + 12,t.dt.minute     );
  strtk::fast::numeric_convert<2>(begin + 15,t.dt.second     );
  strtk::fast::numeric_convert<6>(begin + 18,t.dt.microsecond);
  return true;
strtk_string_to_type_end()

strtk_string_to_type_begin(dt_utils::datetime_format01)
  if (23 != std::distance(begin,end))
    return false;
  else if (
      ('/' != *(begin +  4)) || ('/' != *(begin +  7)) ||
          (' ' != *(begin + 10)) || (':' != *(begin + 13)) ||
          (':' != *(begin + 16)) || ('.' != *(begin + 19))
      )
    return false;
  else if (
      !strtk::fast::all_digits_check<4>(begin +  0) ||
          !strtk::fast::all_digits_check<2>(begin +  5) ||
          !strtk::fast::all_digits_check<2>(begin +  8) ||
          !strtk::fast::all_digits_check<2>(begin + 11) ||
          !strtk::fast::all_digits_check<2>(begin + 14) ||
          !strtk::fast::all_digits_check<2>(begin + 17) ||
          !strtk::fast::all_digits_check<3>(begin + 20)
      )
    return false;
  strtk::fast::numeric_convert<4>(begin +  0,t.dt.year       );
  strtk::fast::numeric_convert<2>(begin +  5,t.dt.month      );
  strtk::fast::numeric_convert<2>(begin +  8,t.dt.day        );
  strtk::fast::numeric_convert<2>(begin + 11,t.dt.hour       );
  strtk::fast::numeric_convert<2>(begin + 14,t.dt.minute     );
  strtk::fast::numeric_convert<2>(begin + 17,t.dt.second     );
  strtk::fast::numeric_convert<3>(begin + 20,t.dt.millisecond);
  return true;
strtk_string_to_type_end()

strtk_string_to_type_begin(dt_utils::datetime_format24)
  if (26 != std::distance(begin,end))
    return false;
  else if (
      ('/' != *(begin +  4)) || ('/' != *(begin +  7)) ||
          (' ' != *(begin + 10)) || (':' != *(begin + 13)) ||
          (':' != *(begin + 16)) || ('.' != *(begin + 19))
      )
    return false;
  else if (
      !strtk::fast::all_digits_check<4>(begin +  0) ||
          !strtk::fast::all_digits_check<2>(begin +  5) ||
          !strtk::fast::all_digits_check<2>(begin +  8) ||
          !strtk::fast::all_digits_check<2>(begin + 11) ||
          !strtk::fast::all_digits_check<2>(begin + 14) ||
          !strtk::fast::all_digits_check<2>(begin + 17) ||
          !strtk::fast::all_digits_check<6>(begin + 20)
      )
    return false;
  strtk::fast::numeric_convert<4>(begin +  0,t.dt.year       );
  strtk::fast::numeric_convert<2>(begin +  5,t.dt.month      );
  strtk::fast::numeric_convert<2>(begin +  8,t.dt.day        );
  strtk::fast::numeric_convert<2>(begin + 11,t.dt.hour       );
  strtk::fast::numeric_convert<2>(begin + 14,t.dt.minute     );
  strtk::fast::numeric_convert<2>(begin + 17,t.dt.second     );
  strtk::fast::numeric_convert<6>(begin + 20,t.dt.microsecond);
  return true;
strtk_string_to_type_end()

strtk_string_to_type_begin(dt_utils::datetime_format02)
  if (23 != std::distance(begin,end))
    return false;
  else if (
      ('/' != *(begin +  2)) || ('/' != *(begin +  5)) ||
          (' ' != *(begin + 10)) || (':' != *(begin + 13)) ||
          (':' != *(begin + 16)) || ('.' != *(begin + 19))
      )
    return false;
  else if (
      !strtk::fast::all_digits_check<2>(begin +  0) ||
          !strtk::fast::all_digits_check<2>(begin +  3) ||
          !strtk::fast::all_digits_check<4>(begin +  6) ||
          !strtk::fast::all_digits_check<2>(begin + 11) ||
          !strtk::fast::all_digits_check<2>(begin + 14) ||
          !strtk::fast::all_digits_check<2>(begin + 17) ||
          !strtk::fast::all_digits_check<3>(begin + 20)
      )
    return false;
  strtk::fast::numeric_convert<2>(begin +  0,t.dt.day        );
  strtk::fast::numeric_convert<2>(begin +  3,t.dt.month      );
  strtk::fast::numeric_convert<4>(begin +  6,t.dt.year       );
  strtk::fast::numeric_convert<2>(begin + 11,t.dt.hour       );
  strtk::fast::numeric_convert<2>(begin + 14,t.dt.minute     );
  strtk::fast::numeric_convert<2>(begin + 17,t.dt.second     );
  strtk::fast::numeric_convert<3>(begin + 20,t.dt.millisecond);
  return true;
strtk_string_to_type_end()

strtk_string_to_type_begin(dt_utils::datetime_format25)
  if (26 != std::distance(begin,end))
    return false;
  else if (
      ('/' != *(begin +  2)) || ('/' != *(begin +  5)) ||
          (' ' != *(begin + 10)) || (':' != *(begin + 13)) ||
          (':' != *(begin + 16)) || ('.' != *(begin + 19))
      )
    return false;
  else if (
      !strtk::fast::all_digits_check<2>(begin +  0) ||
          !strtk::fast::all_digits_check<2>(begin +  3) ||
          !strtk::fast::all_digits_check<4>(begin +  6) ||
          !strtk::fast::all_digits_check<2>(begin + 11) ||
          !strtk::fast::all_digits_check<2>(begin + 14) ||
          !strtk::fast::all_digits_check<2>(begin + 17) ||
          !strtk::fast::all_digits_check<6>(begin + 20)
      )
    return false;
  strtk::fast::numeric_convert<2>(begin +  0,t.dt.day        );
  strtk::fast::numeric_convert<2>(begin +  3,t.dt.month      );
  strtk::fast::numeric_convert<4>(begin +  6,t.dt.year       );
  strtk::fast::numeric_convert<2>(begin + 11,t.dt.hour       );
  strtk::fast::numeric_convert<2>(begin + 14,t.dt.minute     );
  strtk::fast::numeric_convert<2>(begin + 17,t.dt.second     );
  strtk::fast::numeric_convert<6>(begin + 20,t.dt.microsecond);
  return true;
strtk_string_to_type_end()

strtk_string_to_type_begin(dt_utils::datetime_format03)
  if (17 != std::distance(begin,end))
    return false;
  else if (
      (' ' != *(begin +  8)) ||
          (':' != *(begin + 11)) ||
          (':' != *(begin + 14))
      )
    return false;
  else if (
      !strtk::fast::all_digits_check<4>(begin +  0) ||
          !strtk::fast::all_digits_check<2>(begin +  4) ||
          !strtk::fast::all_digits_check<2>(begin +  6) ||
          !strtk::fast::all_digits_check<2>(begin +  9) ||
          !strtk::fast::all_digits_check<2>(begin + 12) ||
          !strtk::fast::all_digits_check<2>(begin + 15)
      )
    return false;
  strtk::fast::numeric_convert<4>(begin +  0,t.dt.year  );
  strtk::fast::numeric_convert<2>(begin +  4,t.dt.month );
  strtk::fast::numeric_convert<2>(begin +  6,t.dt.day   );
  strtk::fast::numeric_convert<2>(begin +  9,t.dt.hour  );
  strtk::fast::numeric_convert<2>(begin + 12,t.dt.minute);
  strtk::fast::numeric_convert<2>(begin + 15,t.dt.second);
  return true;
strtk_string_to_type_end()

strtk_string_to_type_begin(dt_utils::datetime_format04)
  if (19 != std::distance(begin,end))
    return false;
  else if (
      ('/' != *(begin +  4)) || ('/' != *(begin +  7)) ||
          (' ' != *(begin + 10)) || (':' != *(begin + 13)) ||
          (':' != *(begin + 16))
      )
    return false;
  else if (
      !strtk::fast::all_digits_check<4>(begin +  0) ||
          !strtk::fast::all_digits_check<2>(begin +  5) ||
          !strtk::fast::all_digits_check<2>(begin +  8) ||
          !strtk::fast::all_digits_check<2>(begin + 11) ||
          !strtk::fast::all_digits_check<2>(begin + 14) ||
          !strtk::fast::all_digits_check<2>(begin + 17)
      )
    return false;
  strtk::fast::numeric_convert<4>(begin +  0,t.dt.year  );
  strtk::fast::numeric_convert<2>(begin +  5,t.dt.month );
  strtk::fast::numeric_convert<2>(begin +  8,t.dt.day   );
  strtk::fast::numeric_convert<2>(begin + 11,t.dt.hour  );
  strtk::fast::numeric_convert<2>(begin + 14,t.dt.minute);
  strtk::fast::numeric_convert<2>(begin + 17,t.dt.second);
  return true;
strtk_string_to_type_end()

strtk_string_to_type_begin(dt_utils::datetime_format05)
  if (19 != std::distance(begin,end))
    return false;
  else if (
      ('/' != *(begin +  2)) || ('/' != *(begin +  5)) ||
          (' ' != *(begin + 10)) || (':' != *(begin + 13)) ||
          (':' != *(begin + 16))
      )
    return false;
  else if (
      !strtk::fast::all_digits_check<2>(begin +  0) ||
          !strtk::fast::all_digits_check<2>(begin +  3) ||
          !strtk::fast::all_digits_check<4>(begin +  6) ||
          !strtk::fast::all_digits_check<2>(begin + 11) ||
          !strtk::fast::all_digits_check<2>(begin + 14) ||
          !strtk::fast::all_digits_check<2>(begin + 17)
      )
    return false;
  strtk::fast::numeric_convert<2>(begin +  0,t.dt.day   );
  strtk::fast::numeric_convert<2>(begin +  3,t.dt.month );
  strtk::fast::numeric_convert<4>(begin +  6,t.dt.year  );
  strtk::fast::numeric_convert<2>(begin + 11,t.dt.hour  );
  strtk::fast::numeric_convert<2>(begin + 14,t.dt.minute);
  strtk::fast::numeric_convert<2>(begin + 17,t.dt.second);
  return true;
strtk_string_to_type_end()

strtk_string_to_type_begin(dt_utils::datetime_format06)
  if (23 != std::distance(begin,end))
    return false;
  else if (
      ('-' != *(begin +  4)) || ('-' != *(begin +  7)) ||
          (' ' != *(begin + 10)) || (':' != *(begin + 13)) ||
          (':' != *(begin + 16)) || ('.' != *(begin + 19))
      )
    return false;
  else if (
      !strtk::fast::all_digits_check<4>(begin +  0) ||
          !strtk::fast::all_digits_check<2>(begin +  5) ||
          !strtk::fast::all_digits_check<2>(begin +  8) ||
          !strtk::fast::all_digits_check<2>(begin + 11) ||
          !strtk::fast::all_digits_check<2>(begin + 14) ||
          !strtk::fast::all_digits_check<2>(begin + 17) ||
          !strtk::fast::all_digits_check<3>(begin + 20)
      )
    return false;
  strtk::fast::numeric_convert<4>(begin +  0,t.dt.year       );
  strtk::fast::numeric_convert<2>(begin +  5,t.dt.month      );
  strtk::fast::numeric_convert<2>(begin +  8,t.dt.day        );
  strtk::fast::numeric_convert<2>(begin + 11,t.dt.hour       );
  strtk::fast::numeric_convert<2>(begin + 14,t.dt.minute     );
  strtk::fast::numeric_convert<2>(begin + 17,t.dt.second     );
  strtk::fast::numeric_convert<3>(begin + 20,t.dt.millisecond);
  return true;
strtk_string_to_type_end()

strtk_string_to_type_begin(dt_utils::datetime_format26)
  if (26 != std::distance(begin,end))
    return false;
  else if (
      ('-' != *(begin +  4)) || ('-' != *(begin +  7)) ||
          (' ' != *(begin + 10)) || (':' != *(begin + 13)) ||
          (':' != *(begin + 16)) || ('.' != *(begin + 19))
      )
    return false;
  else if (
      !strtk::fast::all_digits_check<4>(begin +  0) ||
          !strtk::fast::all_digits_check<2>(begin +  5) ||
          !strtk::fast::all_digits_check<2>(begin +  8) ||
          !strtk::fast::all_digits_check<2>(begin + 11) ||
          !strtk::fast::all_digits_check<2>(begin + 14) ||
          !strtk::fast::all_digits_check<2>(begin + 17) ||
          !strtk::fast::all_digits_check<6>(begin + 20)
      )
    return false;
  strtk::fast::numeric_convert<4>(begin +  0,t.dt.year       );
  strtk::fast::numeric_convert<2>(begin +  5,t.dt.month      );
  strtk::fast::numeric_convert<2>(begin +  8,t.dt.day        );
  strtk::fast::numeric_convert<2>(begin + 11,t.dt.hour       );
  strtk::fast::numeric_convert<2>(begin + 14,t.dt.minute     );
  strtk::fast::numeric_convert<2>(begin + 17,t.dt.second     );
  strtk::fast::numeric_convert<6>(begin + 20,t.dt.microsecond);
  return true;
strtk_string_to_type_end()

strtk_string_to_type_begin(dt_utils::datetime_format07)
  if (23 != std::distance(begin,end))
    return false;
  else if (
      ('-' != *(begin +  2)) || ('-' != *(begin +  5)) ||
          (' ' != *(begin + 10)) || (':' != *(begin + 13)) ||
          (':' != *(begin + 16)) || ('.' != *(begin + 19))
      )
    return false;
  else if (
      !strtk::fast::all_digits_check<2>(begin +  0) ||
          !strtk::fast::all_digits_check<2>(begin +  3) ||
          !strtk::fast::all_digits_check<4>(begin +  6) ||
          !strtk::fast::all_digits_check<2>(begin + 11) ||
          !strtk::fast::all_digits_check<2>(begin + 14) ||
          !strtk::fast::all_digits_check<2>(begin + 17) ||
          !strtk::fast::all_digits_check<3>(begin + 20)
      )
    return false;
  strtk::fast::numeric_convert<2>(begin +  0,t.dt.day        );
  strtk::fast::numeric_convert<2>(begin +  3,t.dt.month      );
  strtk::fast::numeric_convert<4>(begin +  6,t.dt.year       );
  strtk::fast::numeric_convert<2>(begin + 11,t.dt.hour       );
  strtk::fast::numeric_convert<2>(begin + 14,t.dt.minute     );
  strtk::fast::numeric_convert<2>(begin + 17,t.dt.second     );
  strtk::fast::numeric_convert<3>(begin + 20,t.dt.millisecond);
  return true;
strtk_string_to_type_end()

strtk_string_to_type_begin(dt_utils::datetime_format27)
  if (26 != std::distance(begin,end))
    return false;
  else if (
      ('-' != *(begin +  2)) || ('-' != *(begin +  5)) ||
          (' ' != *(begin + 10)) || (':' != *(begin + 13)) ||
          (':' != *(begin + 16)) || ('.' != *(begin + 19))
      )
    return false;
  else if (
      !strtk::fast::all_digits_check<2>(begin +  0) ||
          !strtk::fast::all_digits_check<2>(begin +  3) ||
          !strtk::fast::all_digits_check<4>(begin +  6) ||
          !strtk::fast::all_digits_check<2>(begin + 11) ||
          !strtk::fast::all_digits_check<2>(begin + 14) ||
          !strtk::fast::all_digits_check<2>(begin + 17) ||
          !strtk::fast::all_digits_check<6>(begin + 20)
      )
    return false;
  strtk::fast::numeric_convert<2>(begin +  0,t.dt.day        );
  strtk::fast::numeric_convert<2>(begin +  3,t.dt.month      );
  strtk::fast::numeric_convert<4>(begin +  6,t.dt.year       );
  strtk::fast::numeric_convert<2>(begin + 11,t.dt.hour       );
  strtk::fast::numeric_convert<2>(begin + 14,t.dt.minute     );
  strtk::fast::numeric_convert<2>(begin + 17,t.dt.second     );
  strtk::fast::numeric_convert<6>(begin + 20,t.dt.microsecond);
  return true;
strtk_string_to_type_end()

strtk_string_to_type_begin(dt_utils::datetime_format08)
  if (19 != std::distance(begin,end))
    return false;
  else if (
      ('-' != *(begin +  4)) || ('-' != *(begin +  7)) ||
          (' ' != *(begin + 10)) || (':' != *(begin + 13)) ||
          (':' != *(begin + 16))
      )
    return false;
  else if (
      !strtk::fast::all_digits_check<4>(begin +  0) ||
          !strtk::fast::all_digits_check<2>(begin +  5) ||
          !strtk::fast::all_digits_check<2>(begin +  8) ||
          !strtk::fast::all_digits_check<2>(begin + 11) ||
          !strtk::fast::all_digits_check<2>(begin + 14) ||
          !strtk::fast::all_digits_check<2>(begin + 17)
      )
    return false;
  strtk::fast::numeric_convert<4>(begin +  0,t.dt.year  );
  strtk::fast::numeric_convert<2>(begin +  5,t.dt.month );
  strtk::fast::numeric_convert<2>(begin +  8,t.dt.day   );
  strtk::fast::numeric_convert<2>(begin + 11,t.dt.hour  );
  strtk::fast::numeric_convert<2>(begin + 14,t.dt.minute);
  strtk::fast::numeric_convert<2>(begin + 17,t.dt.second);
  return true;
strtk_string_to_type_end()

strtk_string_to_type_begin(dt_utils::datetime_format09)
  if (19 != std::distance(begin,end))
    return false;
  else if (
      ('-' != *(begin +  2)) || ('-' != *(begin +  5)) ||
          (' ' != *(begin + 10)) || (':' != *(begin + 13)) ||
          (':' != *(begin + 16))
      )
    return false;
  else if (
      !strtk::fast::all_digits_check<2>(begin +  0) ||
          !strtk::fast::all_digits_check<2>(begin +  3) ||
          !strtk::fast::all_digits_check<4>(begin +  6) ||
          !strtk::fast::all_digits_check<2>(begin + 11) ||
          !strtk::fast::all_digits_check<2>(begin + 14) ||
          !strtk::fast::all_digits_check<2>(begin + 17)
      )
    return false;
  strtk::fast::numeric_convert<2>(begin +  0,t.dt.day   );
  strtk::fast::numeric_convert<2>(begin +  3,t.dt.month );
  strtk::fast::numeric_convert<4>(begin +  6,t.dt.year  );
  strtk::fast::numeric_convert<2>(begin + 11,t.dt.hour  );
  strtk::fast::numeric_convert<2>(begin + 14,t.dt.minute);
  strtk::fast::numeric_convert<2>(begin + 17,t.dt.second);
  return true;
strtk_string_to_type_end()

strtk_string_to_type_begin(dt_utils::datetime_format10)
  if (19 != std::distance(begin,end))
    return false;
  else if (
      ('-' != *(begin +  4)) || ('-' != *(begin +  7)) ||
          ('T' != *(begin + 10)) || (':' != *(begin + 13)) ||
          (':' != *(begin + 16))
      )
    return false;
  else if (
      !strtk::fast::all_digits_check<4>(begin +  0) ||
          !strtk::fast::all_digits_check<2>(begin +  5) ||
          !strtk::fast::all_digits_check<2>(begin +  8) ||
          !strtk::fast::all_digits_check<2>(begin + 11) ||
          !strtk::fast::all_digits_check<2>(begin + 14) ||
          !strtk::fast::all_digits_check<2>(begin + 17)
      )
    return false;
  strtk::fast::numeric_convert<4>(begin +  0,t.dt.year  );
  strtk::fast::numeric_convert<2>(begin +  5,t.dt.month );
  strtk::fast::numeric_convert<2>(begin +  8,t.dt.day   );
  strtk::fast::numeric_convert<2>(begin + 11,t.dt.hour  );
  strtk::fast::numeric_convert<2>(begin + 14,t.dt.minute);
  strtk::fast::numeric_convert<2>(begin + 17,t.dt.second);
  return true;
strtk_string_to_type_end()

strtk_string_to_type_begin(dt_utils::datetime_format11)
  if (23 != std::distance(begin,end))
    return false;
  else if (
      ('-' != *(begin +  4)) || ('-' != *(begin +  7)) ||
          ('T' != *(begin + 10)) || (':' != *(begin + 13)) ||
          (':' != *(begin + 16)) || ('.' != *(begin + 19))
      )
    return false;
  else if (
      !strtk::fast::all_digits_check<4>(begin +  0) ||
          !strtk::fast::all_digits_check<2>(begin +  5) ||
          !strtk::fast::all_digits_check<2>(begin +  8) ||
          !strtk::fast::all_digits_check<2>(begin + 11) ||
          !strtk::fast::all_digits_check<2>(begin + 14) ||
          !strtk::fast::all_digits_check<2>(begin + 17) ||
          !strtk::fast::all_digits_check<3>(begin + 20)
      )
    return false;
  strtk::fast::numeric_convert<4>(begin +  0,t.dt.year       );
  strtk::fast::numeric_convert<2>(begin +  5,t.dt.month      );
  strtk::fast::numeric_convert<2>(begin +  8,t.dt.day        );
  strtk::fast::numeric_convert<2>(begin + 11,t.dt.hour       );
  strtk::fast::numeric_convert<2>(begin + 14,t.dt.minute     );
  strtk::fast::numeric_convert<2>(begin + 17,t.dt.second     );
  strtk::fast::numeric_convert<3>(begin + 20,t.dt.millisecond);
  return true;
strtk_string_to_type_end()

strtk_string_to_type_begin(dt_utils::datetime_format28)
  if (26 != std::distance(begin,end))
    return false;
  else if (
      ('-' != *(begin +  4)) || ('-' != *(begin +  7)) ||
          ('T' != *(begin + 10)) || (':' != *(begin + 13)) ||
          (':' != *(begin + 16)) || ('.' != *(begin + 19))
      )
    return false;
  else if (
      !strtk::fast::all_digits_check<4>(begin +  0) ||
          !strtk::fast::all_digits_check<2>(begin +  5) ||
          !strtk::fast::all_digits_check<2>(begin +  8) ||
          !strtk::fast::all_digits_check<2>(begin + 11) ||
          !strtk::fast::all_digits_check<2>(begin + 14) ||
          !strtk::fast::all_digits_check<2>(begin + 17) ||
          !strtk::fast::all_digits_check<6>(begin + 20)
      )
    return false;
  strtk::fast::numeric_convert<4>(begin +  0,t.dt.year       );
  strtk::fast::numeric_convert<2>(begin +  5,t.dt.month      );
  strtk::fast::numeric_convert<2>(begin +  8,t.dt.day        );
  strtk::fast::numeric_convert<2>(begin + 11,t.dt.hour       );
  strtk::fast::numeric_convert<2>(begin + 14,t.dt.minute     );
  strtk::fast::numeric_convert<2>(begin + 17,t.dt.second     );
  strtk::fast::numeric_convert<6>(begin + 20,t.dt.microsecond);
  return true;
strtk_string_to_type_end()

strtk_string_to_type_begin(dt_utils::datetime_format12)
  if (17 != std::distance(begin,end))
    return false;
  else if (!dt_utils::details::parse_YYYYMMDD(begin,begin + 8,t.dt))
    return false;
  else if (
      ('T' != *(begin +  8)) || (':' != *(begin + 11)) ||
          (':' != *(begin + 14))
      )
    return false;
  else if (
      !strtk::fast::all_digits_check<2>(begin +  9) ||
          !strtk::fast::all_digits_check<2>(begin + 12) ||
          !strtk::fast::all_digits_check<2>(begin + 15)
      )
    return false;
  strtk::fast::numeric_convert<2>(begin +  9,t.dt.hour  );
  strtk::fast::numeric_convert<2>(begin + 12,t.dt.minute);
  strtk::fast::numeric_convert<2>(begin + 15,t.dt.second);
  return true;
strtk_string_to_type_end()

strtk_string_to_type_begin(dt_utils::datetime_format13)
  if (21 != std::distance(begin,end))
    return false;
  else if (!dt_utils::details::parse_YYYYMMDD(begin,begin + 8,t.dt))
    return false;
  else if (
      ('T' != *(begin +  8)) || (':' != *(begin + 11)) ||
          (':' != *(begin + 14))
      )
    return false;
  else if (
      !strtk::fast::all_digits_check<2>(begin +  9) ||
          !strtk::fast::all_digits_check<2>(begin + 12) ||
          !strtk::fast::all_digits_check<2>(begin + 15) ||
          !strtk::fast::all_digits_check<3>(begin + 18)
      )
    return false;
  strtk::fast::numeric_convert<2>(begin +  9,t.dt.hour       );
  strtk::fast::numeric_convert<2>(begin + 12,t.dt.minute     );
  strtk::fast::numeric_convert<2>(begin + 15,t.dt.second     );
  strtk::fast::numeric_convert<3>(begin + 18,t.dt.millisecond);
  return true;
strtk_string_to_type_end()

strtk_string_to_type_begin(dt_utils::datetime_format29)
  if (24 != std::distance(begin,end))
    return false;
  else if (!dt_utils::details::parse_YYYYMMDD(begin,begin + 8,t.dt))
    return false;
  else if (
      ('T' != *(begin +  8)) || (':' != *(begin + 11)) ||
          (':' != *(begin + 14))
      )
    return false;
  else if (
      !strtk::fast::all_digits_check<2>(begin +  9) ||
          !strtk::fast::all_digits_check<2>(begin + 12) ||
          !strtk::fast::all_digits_check<2>(begin + 15) ||
          !strtk::fast::all_digits_check<6>(begin + 18)
      )
    return false;
  strtk::fast::numeric_convert<2>(begin +  9,t.dt.hour       );
  strtk::fast::numeric_convert<2>(begin + 12,t.dt.minute     );
  strtk::fast::numeric_convert<2>(begin + 15,t.dt.second     );
  strtk::fast::numeric_convert<6>(begin + 18,t.dt.microsecond);
  return true;
strtk_string_to_type_end()

strtk_string_to_type_begin(dt_utils::datetime_format14)
  if (23 != std::distance(begin,end))
    return false;
  else if (
      ('-' != *(begin +  2)) || ('-' != *(begin +  5)) ||
          ('T' != *(begin + 10)) || (':' != *(begin + 13)) ||
          (':' != *(begin + 16)) || ('.' != *(begin + 19))
      )
    return false;
  else if (
      !strtk::fast::all_digits_check<2>(begin +  0) ||
          !strtk::fast::all_digits_check<2>(begin +  3) ||
          !strtk::fast::all_digits_check<4>(begin +  6) ||
          !strtk::fast::all_digits_check<2>(begin + 11) ||
          !strtk::fast::all_digits_check<2>(begin + 14) ||
          !strtk::fast::all_digits_check<2>(begin + 17) ||
          !strtk::fast::all_digits_check<3>(begin + 20)
      )
    return false;
  strtk::fast::numeric_convert<2>(begin +  0,t.dt.day        );
  strtk::fast::numeric_convert<2>(begin +  3,t.dt.month      );
  strtk::fast::numeric_convert<4>(begin +  6,t.dt.year       );
  strtk::fast::numeric_convert<2>(begin + 11,t.dt.hour       );
  strtk::fast::numeric_convert<2>(begin + 14,t.dt.minute     );
  strtk::fast::numeric_convert<2>(begin + 17,t.dt.second     );
  strtk::fast::numeric_convert<3>(begin + 20,t.dt.millisecond);
  return true;
strtk_string_to_type_end()

strtk_string_to_type_begin(dt_utils::datetime_format30)
  if (26 != std::distance(begin,end))
    return false;
  else if (
      ('-' != *(begin +  2)) || ('-' != *(begin +  5)) ||
          ('T' != *(begin + 10)) || (':' != *(begin + 13)) ||
          (':' != *(begin + 16)) || ('.' != *(begin + 19))
      )
    return false;
  else if (
      !strtk::fast::all_digits_check<2>(begin +  0) ||
          !strtk::fast::all_digits_check<2>(begin +  3) ||
          !strtk::fast::all_digits_check<4>(begin +  6) ||
          !strtk::fast::all_digits_check<2>(begin + 11) ||
          !strtk::fast::all_digits_check<2>(begin + 14) ||
          !strtk::fast::all_digits_check<2>(begin + 17) ||
          !strtk::fast::all_digits_check<6>(begin + 20)
      )
    return false;
  strtk::fast::numeric_convert<2>(begin +  0,t.dt.day        );
  strtk::fast::numeric_convert<2>(begin +  3,t.dt.month      );
  strtk::fast::numeric_convert<4>(begin +  6,t.dt.year       );
  strtk::fast::numeric_convert<2>(begin + 11,t.dt.hour       );
  strtk::fast::numeric_convert<2>(begin + 14,t.dt.minute     );
  strtk::fast::numeric_convert<2>(begin + 17,t.dt.second     );
  strtk::fast::numeric_convert<6>(begin + 20,t.dt.microsecond);
  return true;
strtk_string_to_type_end()

strtk_string_to_type_begin(dt_utils::datetime_format15)
  if (19 != std::distance(begin,end))
    return false;
  else if (
      ('-' != *(begin +  2)) || ('-' != *(begin +  5)) ||
          ('T' != *(begin + 10)) || (':' != *(begin + 13)) ||
          (':' != *(begin + 16))
      )
    return false;
  else if (
      !strtk::fast::all_digits_check<2>(begin +  0) ||
          !strtk::fast::all_digits_check<2>(begin +  3) ||
          !strtk::fast::all_digits_check<4>(begin +  6) ||
          !strtk::fast::all_digits_check<2>(begin + 11) ||
          !strtk::fast::all_digits_check<2>(begin + 14) ||
          !strtk::fast::all_digits_check<2>(begin + 17)
      )
    return false;
  strtk::fast::numeric_convert<2>(begin +  0,t.dt.day   );
  strtk::fast::numeric_convert<2>(begin +  3,t.dt.month );
  strtk::fast::numeric_convert<4>(begin +  6,t.dt.year  );
  strtk::fast::numeric_convert<2>(begin + 11,t.dt.hour  );
  strtk::fast::numeric_convert<2>(begin + 14,t.dt.minute);
  strtk::fast::numeric_convert<2>(begin + 17,t.dt.second);
  return true;
strtk_string_to_type_end()

strtk_string_to_type_begin(dt_utils::datetime_format16)
  if (13 != std::distance(begin,end))
    return false;
  else if (!dt_utils::details::parse_YYYYMMDD(begin,begin + 8,t.dt))
    return false;
  else if ('T' != *(begin + 8))
    return false;
  else if (
      !strtk::fast::all_digits_check<2>(begin +  9) ||
          !strtk::fast::all_digits_check<2>(begin + 11)
      )
    return false;
  strtk::fast::numeric_convert<2>(begin +  9,t.dt.hour  );
  strtk::fast::numeric_convert<2>(begin + 11,t.dt.minute);
  return true;
strtk_string_to_type_end()

strtk_string_to_type_begin(dt_utils::datetime_format17)
  if (15 != std::distance(begin,end))
    return false;
  else if (!dt_utils::details::parse_YYYYMMDD(begin,begin + 8,t.dt))
    return false;
  else if ('T' != *(begin + 8))
    return false;
  else if (
      !strtk::fast::all_digits_check<2>(begin +  9) ||
          !strtk::fast::all_digits_check<2>(begin + 11) ||
          !strtk::fast::all_digits_check<2>(begin + 13)
      )
    return false;
  strtk::fast::numeric_convert<2>(begin +  9,t.dt.hour  );
  strtk::fast::numeric_convert<2>(begin + 11,t.dt.minute);
  strtk::fast::numeric_convert<2>(begin + 13,t.dt.second);
  return true;
strtk_string_to_type_end()

strtk_string_to_type_begin(dt_utils::datetime_format18)
  if (18 != std::distance(begin,end))
    return false;
  else if (!dt_utils::details::parse_YYYYMMDD(begin,begin + 8,t.dt))
    return false;
  else if ('T' != *(begin + 8))
    return false;
  else if (
      !strtk::fast::all_digits_check<2>(begin +  9) ||
          !strtk::fast::all_digits_check<2>(begin + 11) ||
          !strtk::fast::all_digits_check<2>(begin + 13) ||
          !strtk::fast::all_digits_check<3>(begin + 15)
      )
    return false;
  strtk::fast::numeric_convert<2>(begin +  9,t.dt.hour       );
  strtk::fast::numeric_convert<2>(begin + 11,t.dt.minute     );
  strtk::fast::numeric_convert<2>(begin + 13,t.dt.second     );
  strtk::fast::numeric_convert<3>(begin + 15,t.dt.millisecond);
  return true;
strtk_string_to_type_end()

strtk_string_to_type_begin(dt_utils::datetime_format31)
  if (21 != std::distance(begin,end))
    return false;
  else if (!dt_utils::details::parse_YYYYMMDD(begin,begin + 8,t.dt))
    return false;
  else if ('T' != *(begin + 8))
    return false;
  else if (
      !strtk::fast::all_digits_check<2>(begin +  9) ||
          !strtk::fast::all_digits_check<2>(begin + 11) ||
          !strtk::fast::all_digits_check<2>(begin + 13) ||
          !strtk::fast::all_digits_check<6>(begin + 15)
      )
    return false;
  strtk::fast::numeric_convert<2>(begin +  9,t.dt.hour       );
  strtk::fast::numeric_convert<2>(begin + 11,t.dt.minute     );
  strtk::fast::numeric_convert<2>(begin + 13,t.dt.second     );
  strtk::fast::numeric_convert<6>(begin + 15,t.dt.microsecond);
  return true;
strtk_string_to_type_end()

strtk_string_to_type_begin(dt_utils::datetime_format19)
  const auto size = static_cast<std::size_t>(std::distance(begin,end));
  if ((20 != size) && (25 != size))
    return false;
  else if (
      ('-' != *(begin +  4)) || ('-' != *(begin +  7)) ||
          (!('T' == *(begin + 10) || ' ' == *(begin + 10))) || (':' != *(begin + 13)) ||
          (':' != *(begin + 16))
      )
    return false;
  else if ((19 == size) && ('Z' != *(begin + 19)))
    return false;
  else if (
      (25 == size) &&
          (
              (('-' != *(begin + 19)) && ('+' != *(begin + 19)))
                  ||
                      (':' != *(begin + 22))
          )
      )
    return false;
  else if (
      !strtk::fast::all_digits_check<4>(begin +  0) ||
          !strtk::fast::all_digits_check<2>(begin +  5) ||
          !strtk::fast::all_digits_check<2>(begin +  8) ||
          !strtk::fast::all_digits_check<2>(begin + 11) ||
          !strtk::fast::all_digits_check<2>(begin + 14) ||
          !strtk::fast::all_digits_check<2>(begin + 17)
      )
    return false;
  strtk::fast::numeric_convert<4>(begin +  0,t.dt.year  );
  strtk::fast::numeric_convert<2>(begin +  5,t.dt.month );
  strtk::fast::numeric_convert<2>(begin +  8,t.dt.day   );
  strtk::fast::numeric_convert<2>(begin + 11,t.dt.hour  );
  strtk::fast::numeric_convert<2>(begin + 14,t.dt.minute);
  strtk::fast::numeric_convert<2>(begin + 17,t.dt.second);

  if (20 == size)
    t.dt.tzd = 0;
  else if (25 == size)
  {
    if (
        !strtk::fast::all_digits_check<2>(begin + 20) ||
            !strtk::fast::all_digits_check<2>(begin + 23)
        )
      return false;
    unsigned short tzd_hh;
    unsigned short tzd_mm;
    strtk::fast::numeric_convert<2>(begin + 20,tzd_hh);
    strtk::fast::numeric_convert<2>(begin + 23,tzd_mm);
    t.dt.tzd = ((tzd_hh * 60)  + tzd_mm) * (('-' == *(begin + 19)) ? -1 : 1);
  }
  return true;
strtk_string_to_type_end()

strtk_string_to_type_begin(dt_utils::datetime_format32)
  const auto size = static_cast<std::size_t>(std::distance(begin,end));
  if ((24 != size) && (29 != size))
    return false;
  else if (
      ('-' != *(begin +  4)) || ('-' != *(begin +  7)) ||
          (!('T' == *(begin + 10) || ' ' == *(begin + 10))) || (':' != *(begin + 13)) ||
          (':' != *(begin + 16)) || ('.' != *(begin + 19))
      )
    return false;
  else if ((23 == size) && ('Z' != *(begin + 23)))
    return false;
  else if (
      (29 == size) &&
          (
              (('-' != *(begin + 23)) && ('+' != *(begin + 23)))
                  ||
                      (':' != *(begin + 26))
          )
      )
    return false;
  else if (
      !strtk::fast::all_digits_check<4>(begin +  0) ||
          !strtk::fast::all_digits_check<2>(begin +  5) ||
          !strtk::fast::all_digits_check<2>(begin +  8) ||
          !strtk::fast::all_digits_check<2>(begin + 11) ||
          !strtk::fast::all_digits_check<2>(begin + 14) ||
          !strtk::fast::all_digits_check<2>(begin + 17) ||
          !strtk::fast::all_digits_check<3>(begin + 20)
      )
    return false;
  strtk::fast::numeric_convert<4>(begin +  0,t.dt.year  );
  strtk::fast::numeric_convert<2>(begin +  5,t.dt.month );
  strtk::fast::numeric_convert<2>(begin +  8,t.dt.day   );
  strtk::fast::numeric_convert<2>(begin + 11,t.dt.hour  );
  strtk::fast::numeric_convert<2>(begin + 14,t.dt.minute);
  strtk::fast::numeric_convert<2>(begin + 17,t.dt.second);
  strtk::fast::numeric_convert<3>(begin + 20,t.dt.millisecond);

  if (24 == size)
    t.dt.tzd = 0;
  else if (29 == size)
  {
    if (
        !strtk::fast::all_digits_check<2>(begin + 24) ||
            !strtk::fast::all_digits_check<2>(begin + 27)
        )
      return false;
    unsigned short tzd_hh;
    unsigned short tzd_mm;
    strtk::fast::numeric_convert<2>(begin + 24,tzd_hh);
    strtk::fast::numeric_convert<2>(begin + 27,tzd_mm);
    t.dt.tzd = ((tzd_hh * 60)  + tzd_mm) * (('-' == *(begin + 23)) ? -1 : 1);
  }
  return true;
strtk_string_to_type_end()

strtk_string_to_type_begin(dt_utils::datetime_format33)
  const auto size = static_cast<std::size_t>(std::distance(begin,end));
  if ((27 != size) && (32 != size))
    return false;
  else if (
      ('-' != *(begin +  4)) || ('-' != *(begin +  7)) ||
          (!('T' == *(begin + 10) || ' ' == *(begin + 10))) || (':' != *(begin + 13)) ||
          (':' != *(begin + 16)) || ('.' != *(begin + 19))
      )
    return false;
  else if ((26 == size) && ('Z' != *(begin + 26)))
    return false;
  else if (
      (32 == size) &&
          (
              (('-' != *(begin + 26)) && ('+' != *(begin + 26)))
                  ||
                      (':' != *(begin + 29))
          )
      )
    return false;
  else if (
      !strtk::fast::all_digits_check<4>(begin +  0) ||
          !strtk::fast::all_digits_check<2>(begin +  5) ||
          !strtk::fast::all_digits_check<2>(begin +  8) ||
          !strtk::fast::all_digits_check<2>(begin + 11) ||
          !strtk::fast::all_digits_check<2>(begin + 14) ||
          !strtk::fast::all_digits_check<2>(begin + 17) ||
          !strtk::fast::all_digits_check<6>(begin + 20)
      )
    return false;
  strtk::fast::numeric_convert<4>(begin +  0,t.dt.year  );
  strtk::fast::numeric_convert<2>(begin +  5,t.dt.month );
  strtk::fast::numeric_convert<2>(begin +  8,t.dt.day   );
  strtk::fast::numeric_convert<2>(begin + 11,t.dt.hour  );
  strtk::fast::numeric_convert<2>(begin + 14,t.dt.minute);
  strtk::fast::numeric_convert<2>(begin + 17,t.dt.second);
  strtk::fast::numeric_convert<6>(begin + 20,t.dt.microsecond);

  if (27 == size)
    t.dt.tzd = 0;
  else if (32 == size)
  {
    if (
        !strtk::fast::all_digits_check<2>(begin + 27) ||
            !strtk::fast::all_digits_check<2>(begin + 30)
        )
      return false;
    unsigned short tzd_hh;
    unsigned short tzd_mm;
    strtk::fast::numeric_convert<2>(begin + 27,tzd_hh);
    strtk::fast::numeric_convert<2>(begin + 30,tzd_mm);
    t.dt.tzd = ((tzd_hh * 60)  + tzd_mm) * (('-' == *(begin + 26)) ? -1 : 1);
  }
  return true;
strtk_string_to_type_end()

strtk_string_to_type_begin(dt_utils::datetime_format20)
  const auto size = static_cast<std::size_t>(std::distance(begin,end));
  if ((17 != size) && (22 != size))
    return false;
  else if (
      ('-' != *(begin +  4)) || ('-' != *(begin +  7)) ||
          (!('T' == *(begin + 10) || ' ' == *(begin + 10))) || (':' != *(begin + 13))
      )
    return false;
  else if ((17 == size) && ('Z' != *(begin + 16)))
    return false;
  else if (
      (22 == size) &&
          (
              (('-' != *(begin + 16)) && ('+' != *(begin + 16)))
                  ||
                      (':' != *(begin + 19))
          )
      )
    return false;
  else if (
      !strtk::fast::all_digits_check<4>(begin +  0) ||
          !strtk::fast::all_digits_check<2>(begin +  5) ||
          !strtk::fast::all_digits_check<2>(begin +  8) ||
          !strtk::fast::all_digits_check<2>(begin + 11) ||
          !strtk::fast::all_digits_check<2>(begin + 14)
      )
    return false;
  strtk::fast::numeric_convert<4>(begin +  0,t.dt.year  );
  strtk::fast::numeric_convert<2>(begin +  5,t.dt.month );
  strtk::fast::numeric_convert<2>(begin +  8,t.dt.day   );
  strtk::fast::numeric_convert<2>(begin + 11,t.dt.hour  );
  strtk::fast::numeric_convert<2>(begin + 14,t.dt.minute);
  if (17 == size)
    t.dt.tzd = 0;
  else if (22 == size)
  {
    if (
        !strtk::fast::all_digits_check<2>(begin + 17) ||
            !strtk::fast::all_digits_check<2>(begin + 20)
        )
      return false;
    unsigned short tzd_hh;
    unsigned short tzd_mm;
    strtk::fast::numeric_convert<2>(begin + 17,tzd_hh);
    strtk::fast::numeric_convert<2>(begin + 20,tzd_mm);
    t.dt.tzd = ((tzd_hh * 60)  + tzd_mm) * (('-' == *(begin + 16)) ? -1 : 1);
  }
  return true;
strtk_string_to_type_end()

strtk_string_to_type_begin(dt_utils::datetime_format21)
  const auto size = static_cast<std::size_t>(std::distance(begin,end));
  if (26 != size)
    return false;
  else if (
      ('/' != *(begin +  2)) || ('/' != *(begin +  6)) ||
          (':' != *(begin + 11)) || (':' != *(begin + 14)) ||
          (':' != *(begin + 17)) || (' ' != *(begin + 20))
      )
    return false;
  else if (
      ('-' != *(begin + 21)) && ('+' != *(begin + 21))
      )
    return false;
  else if (
      !strtk::fast::all_digits_check<2>(begin +  0) ||
          !strtk::fast::all_digits_check<4>(begin +  7) ||
          !strtk::fast::all_digits_check<2>(begin + 12) ||
          !strtk::fast::all_digits_check<2>(begin + 15) ||
          !strtk::fast::all_digits_check<2>(begin + 18) ||
          !strtk::fast::all_digits_check<4>(begin + 22)
      )
    return false;
  strtk::fast::numeric_convert<2>(begin +  0,t.dt.day   );
  strtk::fast::numeric_convert<4>(begin +  7,t.dt.year  );
  strtk::fast::numeric_convert<2>(begin + 12,t.dt.hour  );
  strtk::fast::numeric_convert<2>(begin + 15,t.dt.minute);
  strtk::fast::numeric_convert<2>(begin + 18,t.dt.second);
  unsigned short tzd_hh;
  unsigned short tzd_mm;
  strtk::fast::numeric_convert<2>(begin + 22,tzd_hh);
  strtk::fast::numeric_convert<2>(begin + 24,tzd_mm);
  t.dt.tzd = ((tzd_hh * 60)  + tzd_mm) * (('-' == *(begin + 21)) ? -1 : 1);
  return (0 != (t.dt.month = dt_utils::details::month3chr_to_index(begin + 3)));
strtk_string_to_type_end()

strtk_string_to_type_begin(dt_utils::datetime_format22)
  const std::size_t size = static_cast<std::size_t>(std::distance(begin,end));
  if (
      (27 != size) && (28 != size) &&
          (29 != size) && (31 != size)
      )
    return false;
  else if (
      (' ' != *(begin +  4)) || (' ' != *(begin +  7)) ||
          (' ' != *(begin + 11)) || (' ' != *(begin + 16)) ||
          (':' != *(begin + 19)) || (':' != *(begin + 22)) ||
          (' ' != *(begin + 25))
      )
    return false;
  else if (
      !strtk::fast::all_digits_check<2>(begin +  5) ||
          !strtk::fast::all_digits_check<4>(begin + 12) ||
          !strtk::fast::all_digits_check<2>(begin + 17) ||
          !strtk::fast::all_digits_check<2>(begin + 20) ||
          !strtk::fast::all_digits_check<2>(begin + 23) ||
          (0 == dt_utils::details::dow3chr_to_index(begin))
      )
    return false;
  strtk::fast::numeric_convert<2>(begin +  5,t.dt.day   );
  strtk::fast::numeric_convert<4>(begin + 12,t.dt.year  );
  strtk::fast::numeric_convert<2>(begin + 17,t.dt.hour  );
  strtk::fast::numeric_convert<2>(begin + 20,t.dt.minute);
  strtk::fast::numeric_convert<2>(begin + 23,t.dt.second);
  t.dt.tzd = 0;
  if (27 == size)
  {
    if (!dt_utils::details::miltzd1chr_to_offset(begin + 26,t.dt.tzd))
      return false;
  }
  else if (28 == size)
  {
    if (('U' != *(begin +  26)) || ('T' != *(begin +  27)))
      return false;
  }
  else if (29 == size)
  {
    if (!dt_utils::details::tzd3chr_to_offset(begin + 26,t.dt.tzd))
      return false;
  }
  else
  {
    unsigned short tzd_hh;
    unsigned short tzd_mm;
    strtk::fast::numeric_convert<2>(begin + 27,tzd_hh);
    strtk::fast::numeric_convert<2>(begin + 29,tzd_mm);
    t.dt.tzd = ((tzd_hh * 60)  + tzd_mm) * (('-' == *(begin + 26)) ? -1 : 1);
  }
  return (0 != (t.dt.month = dt_utils::details::month3chr_to_index(begin + 8)));
strtk_string_to_type_end()

// clang-format off

#endif  // CPPUTILS_DATETIME_UTILS_HPP_
