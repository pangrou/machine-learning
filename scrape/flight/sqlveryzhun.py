import MySQLdb


def db_con():
    db = MySQLdb.connect("127.0.0.1",""---------"",""---------"",""---------"")
    cursor = db.cursor()
    return db,cursor

def creat(db,cursor):
    cursor.execute("DROP TABLE IF EXISTS fightInfo")
    sql = """CREATE TABLE fightInfo (
            fcategory varchar(32) DEFAULT NULL COMMENT '类别',
            FlightNo varchar(32) DEFAULT NULL COMMENT '航班号',
            FlightCompany varchar(32) DEFAULT NULL COMMENT '航班信息',
            FlightDepcode varchar(32) DEFAULT NULL COMMENT '出发机场三节码',
            FlightArrcode varchar(32) DEFAULT NULL COMMENT '到达机场三节码',
            FlightDeptimePlanDate datetime DEFAULT NULL COMMENT '计划起飞时间',
            FlightArrtimePlanDate datetime DEFAULT NULL COMMENT '计划到达时间',
            FlightDeptimeReadyDate datetime DEFAULT NULL COMMENT '预计起飞时间',
            FlightArrtimeReadyDate datetime DEFAULT NULL COMMENT '预计到达时间',
            FlightDeptimeDate datetime DEFAULT NULL COMMENT '实际起飞时间',
            FlightArrtimeDate datetime DEFAULT NULL COMMENT '实际到达时间',
            CheckinTable varchar(32) DEFAULT NULL COMMENT '值机柜台',
            BoardGate varchar(32) DEFAULT NULL COMMENT '登机口',
            BaggageID varchar(32) DEFAULT NULL COMMENT '行李转盘',
            BoardState varchar(32) DEFAULT NULL,
            FlightState varchar(32) DEFAULT NULL COMMENT '航班状态',
            FlightHTerminal varchar(32) DEFAULT NULL COMMENT '出发候机楼',
            FlightTerminal varchar(32) DEFAULT NULL COMMENT '到达候机楼',
            org_timezone varchar(32) DEFAULT NULL COMMENT '出发地时区',
            dst_timezone varchar(32) DEFAULT NULL COMMENT '到达地时区',
            FlightDep varchar(32) DEFAULT NULL COMMENT '出发城市',
            FlightArr varchar(32) DEFAULT NULL COMMENT '到达城市',
            FlightWaitData bigint(20) DEFAULT '0', 
            bridge varchar(32) DEFAULT NULL,
            FlightDepAirport varchar(32) DEFAULT NULL COMMENT '出发城市名称',
            FlightArrAirport varchar(32) DEFAULT NULL COMMENT '到达城市名称',
            OntimeRate varchar(32) DEFAULT NULL COMMENT '历史准点率',
            generic varchar(32) DEFAULT NULL COMMENT '机型',
            FlightYear bigint(20) DEFAULT '0' COMMENT '机龄',
            DepWeather varchar(32) DEFAULT NULL COMMENT '出发地天气',
            ArrWeather varchar(32) DEFAULT NULL COMMENT '到达地天气',
            FlightDuration varchar(32) DEFAULT NULL COMMENT '飞行时间',
            distance varchar(32) DEFAULT NULL COMMENT '总里程（公里）',
            depWeatherIcon varchar(128) DEFAULT NULL,
            depWeatherTemper varchar(32) DEFAULT NULL COMMENT '出发地温度',
            arrWeatherIcon varchar(128) DEFAULT NULL,
            arrWeatherTemper varchar(32) DEFAULT NULL COMMENT '到达地温度',
            color varchar(32) DEFAULT NULL,
            TodayTimeRate varchar(32) DEFAULT NULL COMMENT '今日准点率',
            creatTime datetime DEFAULT NULL  COMMENT '创建时间',
            updateTime datetime DEFAULT NULL COMMENT '更新时间',
            fightDate date DEFAULT NULL COMMENT '航班日期',
            KEY flight (FlightNo,fightDate)
            )ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='航班信息'
            """
    cursor.execute(sql)

def closeDb(db):
    db.close()

if __name__ == '__main__':
    db,cursor = db_con()
    creat(db,cursor)
    closeDb(db)

