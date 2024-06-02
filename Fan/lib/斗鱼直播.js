var rule = {
    title:'斗鱼直播',
    host:'https://m.douyu.com',
    homeUrl:'/api/home/mix',//网站的首页链接,用于分类获取和推荐获取
    url:'/api/room/list?page=fypage&type=fyfilter',
    filterable:1,//是否启用分类筛选,
    filter_url:'{{fl.cateId}}',
    filter:{
        "yl":[{"key":"cateId","name":"分类","value":[{"n":"原创IP","v":"ip"},{"n":"一起看","v":"yqk"},{"n":"二次元","v":"ecy"},{"n":"音乐","v":"music"},{"n":"户外","v":"HW"},{"n":"美食","v":"ms"},{"n":"心动派对","v":"xdpd"},{"n":"音遇恋人","v":"yinyu"},{"n":"星秀","v":"xingxiu"},{"n":"心动FM","v":"dtxs"},{"n":"娱乐推荐","v":"yltj"},{"n":"新选","v":"xinxuan"}]}],
        "PCgame":[{"key":"cateId","name":"分类","value":[{"n":"英雄联盟","v":"LOL"},{"n":"热门游戏","v":"rmyx"},{"n":"穿越火线","v":"CF"},{"n":"重生边缘","v":"CSBYOL"},{"n":"无畏契约","v":"VALORANT"},{"n":"CFHD","v":"CFHD"},{"n":"命运方舟","v":"LostArk"},{"n":"DNF","v":"DNF"},{"n":"DOTA2","v":"DOTA2"},{"n":"使命召唤","v":"COD"},{"n":"炉石传说","v":"How"},{"n":"CS2","v":"CounterStrike"},{"n":"lol云顶之弈","v":"ydzhy"},{"n":"魔兽争霸","v":"mszb"},{"n":"魔兽怀旧服","v":"wowclassic"},{"n":"全民街篮","v":"qmjl"},{"n":"自走棋","v":"dota2rpg"},{"n":"传奇","v":"cq"},{"n":"跑跑卡丁车","v":"Popkart"},{"n