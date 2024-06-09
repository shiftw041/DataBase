# shiftw-sql.py 学生课程信息管理系统
from mysql import connector
from mysql.connector import Error

# 1-添加学生信息
def add_student():
    sno = input('请输入学生学号:')
    sname = input('请输入学生姓名:')
    ssex = input('请输入学生性别:')
    sage = int(input('请输入学生年龄:'))
    sdept = input('请输入学生系别:')
    scholarship = input('请输入是否获得奖学金:')
    add_student_sql = "insert into student values('%s','%s','%s',%d,'%s','%s')"\
        %(sno,sname,ssex,sage,sdept,scholarship)
    Cursor.execute(add_student_sql)

# 2-修改学生信息
def change_student():
    print('修改学生信息')
    sno = input('请输入要修改的学生的学号:')
    delete_sql = "delete from student where sno='%s'"%sno
    Cursor.execute(delete_sql)
    print('请输入修改后的学生信息:')
    add_student()

# 3.添加课程信息
def add_course():
    cno = input('请输入课程号:')
    cname = input('请输入课程名:')
    cpno = input('请输入先行课课程号:')
    ccredit = int(input('请输入学分:'))
    add_course_sql = "insert into course values('%s','%s','%s',%d)"%(cno,cname,cpno,ccredit)
    Cursor.execute(add_course_sql)

# 4.修改课程信息
def change_course():
    print('修改课程信息')
    cno = input('请输入要修改的课程的课程号:')
    delete_sql = "delete from course where cno='%s'"%(cno)
    Cursor.execute(delete_sql)
    print('请输入修改后的课程信息:')
    add_course()

# 5.删除没有选课的课程信息
def delete_course_not_chosen():
    print('删除没有选课的课程信息')
    delete_course_sql = "delete from course where cno not in( select cno from sc )"
    Cursor.execute(delete_course_sql)

# 6.录入学生成绩
def add_grades():
    print('录入学生成绩')
    sno = input('请输入学号:')
    cno = input('请输入课程号:')
    grades = int(input('请输入成绩:'))
    write_grades_sql = "insert into sc values('%s','%s',%d)"%(sno,cno,grades)
    Cursor.execute(write_grades_sql)

# 7.修改学生成绩
def change_grades():
    print('修改学生成绩')
    sno = input('请输入要修改的学生的学号:')
    cno = input('请输入要修改的学生的课程号:')
    grade = int(input('请输入要修改的学生成绩:'))
    update_sql =  "update sc set grade=%d where sno='%s' and cno = '%s'"%(grade,sno,cno)
    Cursor.execute(update_sql)

# 8.按系统计学生的平均成绩、最好成绩、最差成绩、优秀率、不及格人数
def grades():
    print('按系统计课程的学生成绩情况')
    # 创建新视图 sg(sno,sname,sdept,cno,cname,grade)
    create_view_sql = "create view sg as \
        select student.sno,sname,sdept,course.cno,cname,grade \
        from student,sc,course where student.sno=sc.sno and course.cno=sc.cno"
    Cursor.execute(create_view_sql)
    print("学生选课成绩如下：")
    print("  sno            sname   sdept cno  cname     grade")
    select_sql = "select * from sg"
    Cursor.execute(select_sql)
    data=Cursor.fetchall()
    for t in data:
        print(t)
    # 按系统计某课程学生的成绩情况
    cno = input('请输入要查询的课程号:')
    print(" sdept  cname    avg                max min goodrate            badnum")
    grades_sql="select sdept,cname,avg(grade),max(grade),min(grade),sum(grade>=90)/count(*),sum(grade<60) \
        from sg where cno='%s' group by sdept"%cno
    Cursor.execute(grades_sql)
    data=Cursor.fetchall()
    for t in data:
        print(t)
    # 删除视图
    drop_view_sql = "drop view sg"
    Cursor.execute(drop_view_sql)

# 9-按系对学生成绩进行排名，同时显示出学生、课程和成绩信息
def rank():
    print('按系排序课程的学生')
    # 创建新视图 sg(sno,sname,sdept,cno,cname,grade)
    create_view_sql = "create view sg as select student.sno,sname,sdept,course.cno,cname,grade \
        from student,sc,course where student.sno=sc.sno and course.cno=sc.cno"
    Cursor.execute(create_view_sql)
    # 按系排序某课程学生的成绩情况
    cname = input('请输入要查询的课程名:')
    rank_sql = "select sdept,sname,cname,grade from sg where cname='%s' \
        order by sdept desc,grade desc"%cname
    Cursor.execute(rank_sql)
    data = Cursor.fetchall()
    print("sdept  sname  cname  grade")
    for t in data:
        print(t)
    # 删除视图
    drop_view_sql = "drop view sg"
    Cursor.execute(drop_view_sql)

# 10-查询学生的基本信息和选课信息
def select_student():
    print('查询学生的基本信息和选课信息')
    sno = input('请输入要查询的学生的学号:')
    select_student_sql ="select student.*,sc.cno,course.cname \
        from student,sc,course where student.sno='%s' \
            and student.sno=sc.sno and sc.cno=course.cno"%sno
    Cursor.execute(select_student_sql)  
    data=Cursor.fetchall()
    print("  sno       sname    ssex sage sdept scholarship cno sname")
    for t in data:
        print(t)

# 11-查询student表
def select_student_sql():
    print('查询student表')
    print("  Sno          Sname  Ssex Sage Sdept Scholarship")
    Cursor.execute('select * from student')
    data=Cursor.fetchall()
    for t in data:
        print(t)

# 12-查询course表
def select_course_sql():
    print('查询course表')
    print(" Cno  Cname   Cpno  Ccredit")
    Cursor.execute('select * from course order by course.Cno')
    data=Cursor.fetchall()
    for t in data:
        print(t)

# 13-查询sc表
def select_sc_sql():
    print('查询sc表')
    print("  Sno         Cno Grade")
    Cursor.execute('select * from sc')
    data=Cursor.fetchall()
    for t in data:
        print(t)

# 数据库连接
def connect_to_database():
    try:
        # 用户选择是否使用默认数据或手动输入
        use_default = input('是否更改数据库连接配置(非开发者本人选是,需本地建立好mysql的相应数据库)(y/n):')
        if use_default.lower() == 'n':
            # 使用默认数据连接数据库
            connection = connector.connect(
                host="localhost",
                user="root",
                password="shiftw041",
                database="S_T_U202112131_test",
                auth_plugin='mysql_native_password'
            )
        else:
            # 手动输入数据库连接数据
            print('''
            请手动输入要连接的数据库信息！！
            ''') 
            host = input("输入数据库主机地址: ")
            user = input("输入数据库用户名: ")
            password = input("输入数据库密码: ")
            database = input("输入数据库名: ")
            # 允许用户选择是否使用默认的认证插件
            use_default_auth_plugin = input("是否使用默认的认证插件 'mysql_native_password'?(y/n): ")
            auth_plugin = 'mysql_native_password' if use_default_auth_plugin.lower() == 'y' else None
            
            connection = connector.connect(
                host=host,
                user=user,
                password=password,
                database=database,
                auth_plugin=auth_plugin
            )
        
        if connection.is_connected():
            print("数据库连接成功!!")
            # 创建数据游标
            cursor = connection.cursor()
            return connection, cursor
        else:
            print("数据库连接失败!!")
            return None, None

    except Error as e:
        print(f"Error: {e}")


# 打印功能菜单
def main_menu():
    print("""
====================================================================
| 欢迎进入学生数据管理系统，请选择功能号回车执行:                       
| 0:退出程序                                                        
| 1:添加学生信息
| 2:修改学生信息
| 3:添加课程信息
| 4:修改课程信息
| 5:删除没有选课的课程信息
| 6:录入学生成绩
| 7:修改学生成绩
| 8:按系统计学生的平均成绩、最好成绩、最差成绩、优秀率、不及格人数
| 9:按系对学生成绩进行排名，同时显示出学生、课程和成绩信息
| 10:查询学生的基本信息和选课信息
| 11:查询学生表
| 12:查询课程表
| 13:查询选课成绩表          
==================================================================== 
    """)

# 读取用户选择
def get_user_option():
    while True:
        try:
            return int(input())
        except ValueError:
            print('请输入有效的数字序号。')

# 使用数据库
def perform_operations():
    # 循环接收用户的操作号
    while True:
        try:
            Opcode = get_user_option()
            # 0.退出程序
            if Opcode == 0:
                break
            elif Opcode < 0 or Opcode > 13:
                print('操作序号输入错误，请重新输入。')
                continue
            # 1.添加学生信息
            if Opcode==1:
                print('添加学生信息')
                add_student()
            # 2.修改学生信息
            elif Opcode==2:
                change_student()
            # 3.添加课程信息
            elif Opcode==3:
                print('添加课程信息')
                add_course()
            # 4.修改课程信息
            elif Opcode==4:
                change_course()
            # 5.删除没有选课的课程信息
            elif Opcode==5:
                delete_course_not_chosen()
            # 6.录入学生成绩
            elif Opcode==6:
                add_grades()
            # 7.修改学生成绩
            elif Opcode==7:
                change_grades()
            # 8.按系统计学生的平均成绩、最好成绩、最差成绩、优秀率、不及格人数
            elif Opcode==8:
                grades()
            # 9.按系对学生成绩进行排名，同时显示出学生、课程和成绩信息
            elif Opcode==9:
                rank()
            # 10.查询学生的基本信息和选课信息
            elif Opcode==10:
                select_student()
            # 11.显示学生表
            elif Opcode==11:
                select_student_sql()
            # 12.显示课程表
            elif Opcode==12:
                select_course_sql()
            # 13.显示选课成绩表
            elif Opcode==13:
                select_sc_sql()    

            # 提交所作的修改到数据库
            Connection.commit()
            print('操作完成')
        except Exception as e:
            # 发生异常时，打印错误信息并回滚事务
            print(f'发生错误：{e}')
            Connection.rollback()
            continue  # 继续执行循环，等待用户下一个输入
        except KeyboardInterrupt:
            # 用户可通过按 Ctrl+C 来中断程序
            print('程序被用户中断。')
            break
        except:
            # 捕获所有其他未预料到的异常
            print('发生了未知错误。')
            Connection.rollback()
            break  # 退出循环，结束程序

if __name__ == '__main__':
    print('''ooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo
      _      _   __  _             
 ___ | |__  (_) / _|| |_ __      __
/ __|| '_ \ | || |_ | __|\ \ /\ / /
\__ \| | | || ||  _|| |_  \ V  V / 
|___/|_| |_||_||_|   \__|  \_/\_/  
          
欢迎使用U202112131-shiftw开发的数据库应用^-^
ooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo
''')  
    # 连接数据库
    Connection, Cursor = connect_to_database()
    # 显示功能菜单
    main_menu()
    # 使用数据库
    perform_operations()
    # 关闭游标和连接
    Cursor.close()
    Connection.close()
    print('数据库连接关闭，退出程序')
    