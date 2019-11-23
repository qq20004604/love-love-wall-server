use mysql;
-- 任意地点的root账号可以用一个非常复杂的密码登录（瞎打的），用于禁止无密码登录
GRANT ALL ON love_love_wall.* to love_wall_admin@'%' identified by 'fewfwefeaiv+_ewaubnweb@${}ergeno341@@$@!' with grant option;
-- mysql新设置用户或权限后需要刷新系统权限否则可能会出现拒绝访问：
FLUSH PRIVILEGES;