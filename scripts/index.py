def process_json_data(cleaned_text):
    try:
        data = json.loads(cleaned_text)
        keys_to_remove = [
            'csp_Dm84', 'csp_Anime1', 'csp_Kugou', 'Aid', '易搜', 'csp_PanSearch', '短视频', 'TgYunPan|本地',
            '纸条搜', '网盘集合', '少儿', '初中', '高中', '小学', 'csp_Bili', '88看球', 'csp_Qiyou', 'csp_Alllive', 
            '有声小说吧', '虎牙直播', 'csp_Local', 'push_agent', 'TgYunPanLocal5', 'csp_FengGo',
            'TgYunPanLocal4', 'TgYunPanLocal3', 'TgYunPanLocal2', 'TgYunPanLocal1', '酷奇MV', '斗鱼直播',
            'Youtube', 'ConfigCenter', 'JRKAN直播', '星剧社', '蜡笔', '玩偶gg', 'csp_YGP', 'csp_SP360'
        ]
        
        # 删除指定 key 的项，并去掉 name 中包含“墙外”或“木偶”的项
        if 'sites' in data:
            data['sites'] = [
                site for site in data['sites'] 
                if site.get('key') not in keys_to_remove and '墙外' not in site.get('name', '') and '木偶' not in site.get('name', '')
            ]

            # 修改指定 key 的 name 字段
            for site in data['sites']:
                if site.get('key') == 'csp_Douban':
                    site['name'] = '🔍豆瓣TOP榜'
                elif site.get('key') == 'csp_DouDou':
                    site['name'] = '🔍豆瓣TOP榜'
                elif site.get('key') == 'csp_Jianpian':
                    site['name'] = '⚡荐片'
                elif site.get('key') == 'csp_SixV':
                    site['name'] = '🌸新6V'

            # 将 "csp_Jianpian" 调整到第二个位置
            jianpian_site = next((site for site in data['sites'] if site.get('key') == 'csp_Jianpian'), None)
            if jianpian_site:
                data['sites'].remove(jianpian_site)
                data['sites'].insert(1, jianpian_site)

        # 替换 "lives" 列表中的内容，保留3组并更新字段值
        if 'lives' in data:
            data['lives'] = [
                {"name": "IPV4", "url": "https://gh.999986.xyz/https://raw.githubusercontent.com/387673116/Tvbox/master/iptv4.m3u"},
                {"name": "IPV6", "url": "https://gh.999986.xyz/https://raw.githubusercontent.com/387673116/Tvbox/master/iptv6.m3u"},
                {"name": "综合频道", "url": "https://gh.999986.xyz/https://raw.githubusercontent.com/387673116/Tvbox/master/zonghe.m3u"}
            ]

        return data

    except json.JSONDecodeError as e:
        print(f"JSON 解析错误: {e}")
        return None
