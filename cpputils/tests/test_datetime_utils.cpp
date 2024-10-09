// Copyright (c) 2024 Semjon Geist.

//
// Created by sgeist on 12.02.24.
//
#include <tests/catch2.hpp>

TEST_CASE("date_format00 YYYYMMDD is correctly parsed", "[datetime]") {
  std::string data = "20060317";
  dt_utils::datetime dt;
  dt_utils::date_format00 dtd00(dt);
  dt.clear();
  REQUIRE(strtk::string_to_type_converter(data, dtd00));
  REQUIRE(dt.year == 2006);
  REQUIRE(dt.month == 3);
  REQUIRE(dt.day == 17);
}

TEST_CASE("date_format01 YYYYDDMM is correctly parsed", "[datetime]") {
  std::string data = "20061703";
  dt_utils::datetime dt;
  dt_utils::date_format01 dtd1(dt);
  dt.clear();
  REQUIRE(strtk::string_to_type_converter(data, dtd1));
  REQUIRE(dt.year == 2006);
  REQUIRE(dt.month == 3);
  REQUIRE(dt.day == 17);
}

TEST_CASE("date_format02 YYYY/MM/DD is correctly parsed", "[datetime]") {
  std::string data = "2006/03/17";
  dt_utils::datetime dt;
  dt_utils::date_format02 dtd2(dt);
  dt.clear();
  REQUIRE(strtk::string_to_type_converter(data, dtd2));
  REQUIRE(dt.year == 2006);
  REQUIRE(dt.month == 3);
  REQUIRE(dt.day == 17);
}

TEST_CASE("date_format03 YYYY/DD/MM is correctly parsed", "[datetime]") {
  std::string data = "2006/17/03";
  dt_utils::datetime dt;
  dt_utils::date_format03 dtd3(dt);
  dt.clear();
  REQUIRE(strtk::string_to_type_converter(data, dtd3));
  REQUIRE(dt.year == 2006);
  REQUIRE(dt.month == 3);
  REQUIRE(dt.day == 17);
}

TEST_CASE("date_format04 DD/MM/YYYY is correctly parsed", "[datetime]") {
  std::string data = "17/03/2006";
  dt_utils::datetime dt;
  dt_utils::date_format04 dtd4(dt);
  dt.clear();
  REQUIRE(strtk::string_to_type_converter(data, dtd4));
  REQUIRE(dt.year == 2006);
  REQUIRE(dt.month == 3);
  REQUIRE(dt.day == 17);
}

TEST_CASE("date_format05 MM/DD/YYYY is correctly parsed", "[datetime]") {
  std::string data = "03/17/2006";
  dt_utils::datetime dt;
  dt_utils::date_format05 dtd5(dt);
  dt.clear();
  REQUIRE(strtk::string_to_type_converter(data, dtd5));
  REQUIRE(dt.year == 2006);
  REQUIRE(dt.month == 3);
  REQUIRE(dt.day == 17);
}

TEST_CASE("date_format06 YYYY-MM-DD is correctly parsed", "[datetime]") {
  std::string data = "2006-03-17";
  dt_utils::datetime dt;
  dt_utils::date_format06 dtd6(dt);
  dt.clear();
  REQUIRE(strtk::string_to_type_converter(data, dtd6));
  REQUIRE(dt.year == 2006);
  REQUIRE(dt.month == 3);
  REQUIRE(dt.day == 17);
}

TEST_CASE("date_format07 YYYY-DD-MM is correctly parsed", "[datetime]") {
  std::string data = "2006-17-03";
  dt_utils::datetime dt;
  dt_utils::date_format07 dtd7(dt);
  dt.clear();
  REQUIRE(strtk::string_to_type_converter(data, dtd7));
  REQUIRE(dt.year == 2006);
  REQUIRE(dt.month == 3);
  REQUIRE(dt.day == 17);
}

TEST_CASE("date_format08 DD-MM-YYYY is correctly parsed", "[datetime]") {
  std::string data = "17-03-2006";
  dt_utils::datetime dt;
  dt_utils::date_format08 dtd8(dt);
  dt.clear();
  REQUIRE(strtk::string_to_type_converter(data, dtd8));
  REQUIRE(dt.year == 2006);
  REQUIRE(dt.month == 3);
  REQUIRE(dt.day == 17);
}

TEST_CASE("datetime_format09 DD-MM-YYYY HH:MM:SS is correctly parsed",
          "[datetime]") {
  std::string data = "17-03-2006 13:27:54";
  dt_utils::datetime dt;
  dt_utils::datetime_format09 dt9(dt);
  dt.clear();
  REQUIRE(strtk::string_to_type_converter(data, dt9));
  REQUIRE(dt.year == 2006);
  REQUIRE(dt.month == 3);
  REQUIRE(dt.day == 17);
  REQUIRE(dt.hour == 13);
  REQUIRE(dt.minute == 27);
  REQUIRE(dt.second == 54);
}

TEST_CASE("datetime_format10 YYYY-MM-DDTHH:MM:SS is correctly parsed",
          "[datetime]") {
  std::string data = "2006-03-17T13:27:54";
  dt_utils::datetime dt;
  dt_utils::datetime_format10 dt10(dt);
  dt.clear();
  REQUIRE(strtk::string_to_type_converter(data, dt10));
  REQUIRE(dt.year == 2006);
  REQUIRE(dt.month == 3);
  REQUIRE(dt.day == 17);
  REQUIRE(dt.hour == 13);
  REQUIRE(dt.minute == 27);
  REQUIRE(dt.second == 54);
}

TEST_CASE("datetime_format11 YYYY-MM-DDTHH:MM:SS.MSS is correctly parsed",
          "[datetime]") {
  std::string data = "2006-03-17T13:27:54.123";
  dt_utils::datetime dt;
  dt_utils::datetime_format11 dt11(dt);
  dt.clear();
  REQUIRE(strtk::string_to_type_converter(data, dt11));
  REQUIRE(dt.year == 2006);
  REQUIRE(dt.month == 3);
  REQUIRE(dt.day == 17);
  REQUIRE(dt.hour == 13);
  REQUIRE(dt.minute == 27);
  REQUIRE(dt.second == 54);
  REQUIRE(dt.millisecond == 123);
}

TEST_CASE("datetime_format12 YYYYMMDDTHH:MM:SS is correctly parsed",
          "[datetime]") {
  std::string data = "20060317T13:27:54";
  dt_utils::datetime dt;
  dt_utils::datetime_format12 dt12(dt);
  dt.clear();
  REQUIRE(strtk::string_to_type_converter(data, dt12));
  REQUIRE(dt.year == 2006);
  REQUIRE(dt.month == 3);
  REQUIRE(dt.day == 17);
  REQUIRE(dt.hour == 13);
  REQUIRE(dt.minute == 27);
  REQUIRE(dt.second == 54);
}

TEST_CASE("datetime_format13 YYYYMMDDTHH:MM:SS.MSS is correctly parsed",
          "[datetime]") {
  std::string data = "20060317T13:27:54.123";
  dt_utils::datetime dt;
  dt_utils::datetime_format13 dt13(dt);
  dt.clear();
  REQUIRE(strtk::string_to_type_converter(data, dt13));
  REQUIRE(dt.year == 2006);
  REQUIRE(dt.month == 3);
  REQUIRE(dt.day == 17);
  REQUIRE(dt.hour == 13);
  REQUIRE(dt.minute == 27);
  REQUIRE(dt.second == 54);
  REQUIRE(dt.millisecond == 123);
}

TEST_CASE("datetime_format14 DD-MM-YYYYTHH:MM:SS.MSS is correctly parsed",
          "[datetime]") {
  std::string data = "17-03-2006T13:27:54.123";
  dt_utils::datetime dt;
  dt_utils::datetime_format14 dt14(dt);
  dt.clear();
  REQUIRE(strtk::string_to_type_converter(data, dt14));
  REQUIRE(dt.year == 2006);
  REQUIRE(dt.month == 3);
  REQUIRE(dt.day == 17);
  REQUIRE(dt.hour == 13);
  REQUIRE(dt.minute == 27);
  REQUIRE(dt.second == 54);
  REQUIRE(dt.millisecond == 123);
}

TEST_CASE("datetime_format15 DD-MM-YYYYTHH:MM:SS is correctly parsed",
          "[datetime]") {
  std::string data = "17-03-2006T13:27:54";
  dt_utils::datetime dt;
  dt_utils::datetime_format15 dt15(dt);
  dt.clear();
  REQUIRE(strtk::string_to_type_converter(data, dt15));
  REQUIRE(dt.year == 2006);
  REQUIRE(dt.month == 3);
  REQUIRE(dt.day == 17);
  REQUIRE(dt.hour == 13);
  REQUIRE(dt.minute == 27);
  REQUIRE(dt.second == 54);
}

TEST_CASE("datetime_format16 YYYYMMDDTHHMM is correctly parsed", "[datetime]") {
  std::string data = "20060317T1327";
  dt_utils::datetime dt;
  dt_utils::datetime_format16 dt16(dt);
  dt.clear();
  REQUIRE(strtk::string_to_type_converter(data, dt16));
  REQUIRE(dt.year == 2006);
  REQUIRE(dt.month == 3);
  REQUIRE(dt.day == 17);
  REQUIRE(dt.hour == 13);
  REQUIRE(dt.minute == 27);
}

TEST_CASE("datetime_format17 YYYYMMDDTHHMMSS is correctly parsed",
          "[datetime]") {
  std::string data = "20060317T132754";
  dt_utils::datetime dt;
  dt_utils::datetime_format17 dt17(dt);
  dt.clear();
  REQUIRE(strtk::string_to_type_converter(data, dt17));
  REQUIRE(dt.year == 2006);
  REQUIRE(dt.month == 3);
  REQUIRE(dt.day == 17);
  REQUIRE(dt.hour == 13);
  REQUIRE(dt.minute == 27);
  REQUIRE(dt.second == 54);
}

TEST_CASE("datetime_format18 YYYYMMDDTHHMMMSS is correctly parsed",
          "[datetime]") {
  std::string data = "20060317T132754123";
  dt_utils::datetime dt;
  dt_utils::datetime_format18 dt18(dt);
  dt.clear();
  REQUIRE(strtk::string_to_type_converter(data, dt18));
  REQUIRE(dt.year == 2006);
  REQUIRE(dt.month == 3);
  REQUIRE(dt.day == 17);
  REQUIRE(dt.hour == 13);
  REQUIRE(dt.minute == 27);
  REQUIRE(dt.second == 54);
  REQUIRE(dt.millisecond == 123);
}

TEST_CASE("datetime_format19 ISO8601 + py DateThh:mm:ssTZD is correctly parsed",
          "[datetime]") {
  std::string data = "2006-03-17T13:27:54Z";
  dt_utils::datetime dt;
  dt_utils::datetime_format19 dt19(dt);
  dt.clear();
  REQUIRE(strtk::string_to_type_converter(data, dt19));
  REQUIRE(dt.year == 2006);
  REQUIRE(dt.month == 3);
  REQUIRE(dt.day == 17);
  REQUIRE(dt.hour == 13);
  REQUIRE(dt.minute == 27);
  REQUIRE(dt.second == 54);
  REQUIRE(dt.tzd == 0);
}

TEST_CASE("datetime_format20 ISO8601 + py DateThh:mmTZD is correctly parsed",
          "[datetime]") {
  std::string data = "2006-03-17T13:27Z";
  dt_utils::datetime dt;
  dt_utils::datetime_format20 dt20(dt);
  dt.clear();
  REQUIRE(strtk::string_to_type_converter(data, dt20));
  REQUIRE(dt.year == 2006);
  REQUIRE(dt.month == 3);
  REQUIRE(dt.day == 17);
  REQUIRE(dt.hour == 13);
  REQUIRE(dt.minute == 27);
  REQUIRE(dt.tzd == 0);
}

TEST_CASE("datetime_format21 NCSA CLF is correctly parsed", "[datetime]") {
  std::string data = "17/Mar/2006:13:27:54 -0537";
  dt_utils::datetime dt;
  dt_utils::datetime_format21 dt21(dt);
  dt.clear();
  REQUIRE(strtk::string_to_type_converter(data, dt21));
  REQUIRE(dt.year == 2006);
  REQUIRE(dt.month == 3);
  REQUIRE(dt.day == 17);
  REQUIRE(dt.hour == 13);
  REQUIRE(dt.minute == 27);
  REQUIRE(dt.second == 54);
  REQUIRE(dt.tzd == -337);
}

TEST_CASE("datetime_format22 RFC-822(5) is correctly parsed", "[datetime]") {
  std::string data = "Sat, 17 Mar 2006 13:27:54 +0325";
  dt_utils::datetime dt;
  dt_utils::datetime_format22 dt22(dt);
  dt.clear();
  REQUIRE(strtk::string_to_type_converter(data, dt22));
  REQUIRE(dt.year == 2006);
  REQUIRE(dt.month == 3);
  REQUIRE(dt.day == 17);
  REQUIRE(dt.hour == 13);
  REQUIRE(dt.minute == 27);
  REQUIRE(dt.second == 54);
  REQUIRE(dt.tzd == +205);
}

TEST_CASE("datetime_format23 YYYYMMDD HH:MM:SS.mcss  is correctly parsed",
          "[datetime]") {
  std::string data = "20060317 13:27:54.123456";
  dt_utils::datetime dt;
  dt_utils::datetime_format23 dt23(dt);
  dt.clear();
  REQUIRE(strtk::string_to_type_converter(data, dt23));
  REQUIRE(dt.year == 2006);
  REQUIRE(dt.month == 3);
  REQUIRE(dt.day == 17);
  REQUIRE(dt.hour == 13);
  REQUIRE(dt.minute == 27);
  REQUIRE(dt.second == 54);
  REQUIRE(dt.microsecond == 123456);
}

TEST_CASE("datetime_format24 YYYY/MM/DD HH:MM:SS.mcss is correctly parsed",
          "[datetime]") {
  std::string data = "2006/03/17 13:27:54.123456";
  dt_utils::datetime dt;
  dt_utils::datetime_format24 dt24(dt);
  dt.clear();
  REQUIRE(strtk::string_to_type_converter(data, dt24));
  REQUIRE(dt.year == 2006);
  REQUIRE(dt.month == 3);
  REQUIRE(dt.day == 17);
  REQUIRE(dt.hour == 13);
  REQUIRE(dt.minute == 27);
  REQUIRE(dt.second == 54);
  REQUIRE(dt.microsecond == 123456);
}

TEST_CASE("datetime_format25 DD/MM/YYYY HH:MM:SS.mcss is correctly parsed",
          "[datetime]") {
  std::string data = "17/03/2006 13:27:54.123456";
  dt_utils::datetime dt;
  dt_utils::datetime_format25 dt25(dt);
  dt.clear();
  REQUIRE(strtk::string_to_type_converter(data, dt25));
  REQUIRE(dt.year == 2006);
  REQUIRE(dt.month == 3);
  REQUIRE(dt.day == 17);
  REQUIRE(dt.hour == 13);
  REQUIRE(dt.minute == 27);
  REQUIRE(dt.second == 54);
  REQUIRE(dt.microsecond == 123456);
}

TEST_CASE("datetime_format26 YYYY-MM-DD HH:MM:SS.mss is correctly parsed",
          "[datetime]") {
  std::string data = "2006-03-17 13:27:54.123456";
  dt_utils::datetime dt;
  dt_utils::datetime_format26 dt26(dt);
  dt.clear();
  REQUIRE(strtk::string_to_type_converter(data, dt26));
  REQUIRE(dt.year == 2006);
  REQUIRE(dt.month == 3);
  REQUIRE(dt.day == 17);
  REQUIRE(dt.hour == 13);
  REQUIRE(dt.minute == 27);
  REQUIRE(dt.second == 54);
  REQUIRE(dt.microsecond == 123456);
}

TEST_CASE("datetime_format27 DD-MM-YYYY HH:MM:SS.mss is correctly parsed",
          "[datetime]") {
  std::string data = "17-03-2006 13:27:54.123456";
  dt_utils::datetime dt;
  dt_utils::datetime_format27 dt27(dt);
  dt.clear();
  REQUIRE(strtk::string_to_type_converter(data, dt27));
  REQUIRE(dt.year == 2006);
  REQUIRE(dt.month == 3);
  REQUIRE(dt.day == 17);
  REQUIRE(dt.hour == 13);
  REQUIRE(dt.minute == 27);
  REQUIRE(dt.second == 54);
  REQUIRE(dt.microsecond == 123456);
}

TEST_CASE("datetime_format28 YYYY-MM-DDTHH:MM:SS.mss is correctly parsed",
          "[datetime]") {
  std::string data = "2006-03-17T13:27:54.123456";
  dt_utils::datetime dt;
  dt_utils::datetime_format28 dt28(dt);
  dt.clear();
  REQUIRE(strtk::string_to_type_converter(data, dt28));
  REQUIRE(dt.year == 2006);
  REQUIRE(dt.month == 3);
  REQUIRE(dt.day == 17);
  REQUIRE(dt.hour == 13);
  REQUIRE(dt.minute == 27);
  REQUIRE(dt.second == 54);
  REQUIRE(dt.microsecond == 123456);
}

TEST_CASE("datetime_format29 YYYYMMDDTHH:MM:SS.mcss is correctly parsed",
          "[datetime]") {
  std::string data = "20060317T13:27:54.123456";
  dt_utils::datetime dt;
  dt_utils::datetime_format29 dt29(dt);
  dt.clear();
  REQUIRE(strtk::string_to_type_converter(data, dt29));
  REQUIRE(dt.year == 2006);
  REQUIRE(dt.month == 3);
  REQUIRE(dt.day == 17);
  REQUIRE(dt.hour == 13);
  REQUIRE(dt.minute == 27);
  REQUIRE(dt.second == 54);
  REQUIRE(dt.microsecond == 123456);
}

TEST_CASE("datetime_format30 DD-MM-YYYYTHH:MM:SS.mcss is correctly parsed",
          "[datetime]") {
  std::string data = "17-03-2006T13:27:54.123456";
  dt_utils::datetime dt;
  dt_utils::datetime_format30 dt30(dt);
  dt.clear();
  REQUIRE(strtk::string_to_type_converter(data, dt30));
  REQUIRE(dt.year == 2006);
  REQUIRE(dt.month == 3);
  REQUIRE(dt.day == 17);
  REQUIRE(dt.hour == 13);
  REQUIRE(dt.minute == 27);
  REQUIRE(dt.second == 54);
  REQUIRE(dt.microsecond == 123456);
}

TEST_CASE("datetime_format31 YYYYMMDDTHHMMSSNSS is correctly parsed",
          "[datetime]") {
  std::string data = "20060317T132754123456";
  dt_utils::datetime dt;
  dt_utils::datetime_format31 dt31(dt);
  dt.clear();
  REQUIRE(strtk::string_to_type_converter(data, dt31));
  REQUIRE(dt.year == 2006);
  REQUIRE(dt.month == 3);
  REQUIRE(dt.day == 17);
  REQUIRE(dt.hour == 13);
  REQUIRE(dt.minute == 27);
  REQUIRE(dt.second == 54);
  REQUIRE(dt.microsecond == 123456);
}

TEST_CASE("datetime_format32 ISO8601 DateThh:mm:ss.mssTZD is correctly parsed",
          "[datetime]") {
  std::string data = "2006-03-17T15:45:30.123+02:00";
  dt_utils::datetime dt;
  dt_utils::datetime_format32 dt32(dt);
  dt.clear();
  REQUIRE(strtk::string_to_type_converter(data, dt32));
  REQUIRE(dt.year == 2006);
  REQUIRE(dt.month == 3);
  REQUIRE(dt.day == 17);
  REQUIRE(dt.hour == 15);
  REQUIRE(dt.minute == 45);
  REQUIRE(dt.second == 30);
  REQUIRE(dt.millisecond == 123);
  REQUIRE(dt.tzd == 120);
}

TEST_CASE("datetime_format33 ISO8601 DateThh:mm:ss.mcssTZD is correctly parsed",
          "[datetime]") {
  std::string data = "2006-03-17T13:27:54.123456+02:00";
  dt_utils::datetime dt;
  dt_utils::datetime_format33 dt33(dt);
  dt.clear();
  REQUIRE(strtk::string_to_type_converter(data, dt33));
  REQUIRE(dt.year == 2006);
  REQUIRE(dt.month == 3);
  REQUIRE(dt.day == 17);
  REQUIRE(dt.hour == 13);
  REQUIRE(dt.minute == 27);
  REQUIRE(dt.second == 54);
  REQUIRE(dt.microsecond == 123456);
  REQUIRE(dt.tzd == 120);
}
