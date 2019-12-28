adminMenus = {
  'log':[
    {'name':'日志搜索', 'children':[{'name':'快速检索','path':'/log/search','icon':'fa fa-search'}]},
    {'name':'日志分析', 'children':[{'name':'业务分析','path':'/log/analysis','icon':'fa fa-area-chart'}]},
    {'name':'日志接入', 'children':[{'name':'快速接入','path':'/log/join','icon':'fa fa-anchor'},
                               {'name':'日志转发','path':'/log/transmit','icon':'fa fa-rocket'}]},
    {'name':'日志告警', 'children':[{'name':'告警设置','path':'/log/alarmset','icon':'fa fa-cogs'},
                               {'name':'告警列表','path':'/log/alarmlist','icon':'fa fa-bell'}]},
  ],
  'admin':[
    {'name':'业务配置', 'children':[{'name':'业务管理','path':'/admin/business','icon':'fa fa-cube'},
                               {'name':'主机管理','path':'/admin/host','icon':'fa fa-laptop'},
                               {'name':'日志结构化','path':'/admin/structure','icon':'fa fa-map-o'},]},
    {'name':'系统配置', 'children':[{'name':'用户管理','path':'/admin/user','icon':'fa fa-user'},
                                {'name':'角色管理','path':'/admin/role','icon':'fa fa-users'},
                                {'name':'数据源','path':'/admin/newDatasource','icon':'fa fa-database'},
                                {'name':'系统设置','path':'/admin/system','icon':'fa fa-cogs'}]},
    {'name':'个人中心', 'children':[{'name':'个人信息','path':'/admin/userprofile','icon':'fa fa-info-circle'}],'signOut':True}
  ]
}

normalMenus = {
  'log':[
    {'name':'日志搜索', 'children':[{'name':'快速检索','path':'/log/search','icon':'fa fa-search'}]},
    {'name':'日志分析', 'children':[{'name':'业务分析','path':'/log/analysis','icon':'fa fa-area-chart'}]},
    {'name':'日志告警', 'children':[{'name':'告警设置','path':'/log/alarmset','icon':'fa fa-cogs'},
                               {'name':'告警列表','path':'/log/alarmlist','icon':'fa fa-bell'}]}
  ],
  'admin':[
    {'name':'个人中心', 'children':[{'name':'个人信息','path':'/admin/userprofile','icon':'fa fa-info-circle'}],'signOut':True}
  ]
}

def get_menus(role):
    if role:
        return adminMenus
    else:
        return normalMenus