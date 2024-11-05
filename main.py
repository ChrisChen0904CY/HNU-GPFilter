import requests
import json

def getInfo(authorization):
    url = "http://hdjw.hnu.edu.cn/graduation/jwxtpt/v1/bysj/xsdZzmt/findXsdxtControler"
    headers = {
        "Accept": "application/json, text/plain, */*",
        "Authorization": authorization,  
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36 Edg/130.0.0.0",
        "Origin": "http://hdjw.hnu.edu.cn",
        "Referer": "http://hdjw.hnu.edu.cn/graduation/bysj/student/selected-topic/index"
    }
    
    payload = {
        "byjb": "2025",
        "ktmc": "",
        "jsxm": "",
        "ktsylx": "1",
        "ktrs": "2",
        "page": {
            "pageIndex": 1,
            "pageSize": 300
        }
    }

    response = requests.post(url, headers=headers, json=payload)

    if response.status_code == 200:
        data = response.json()
        # 处理返回的 JSON 数据
        return data
    else:
        print(f"请求失败，状态码：{response.status_code}")
        
def generate_HTML(info_list):
    # 统计每个研究方向的数量
    research_directions = {}

    for item in info_list:
        yjfx = item.get('yjfx', '未提供研究方向')  # 获取研究方向
        if yjfx not in research_directions:
            research_directions[yjfx] = 0
        research_directions[yjfx] += 1

    # 生成研究方向目录的HTML
    research_direction_html = '<ul class="research-tree">'
    
    for direction, count in research_directions.items():
        research_direction_html += f'''
            <li class="research-item" onclick="filterByDirection('{direction}')">
                {direction} ({count})
            </li>
        '''
    research_direction_html += '</ul>'
    
    # 生成HTML内容
    html_content = '''
    <!DOCTYPE html>
    <html lang="zh">
    <head>
      <meta charset="UTF-8">
      <meta name="viewport" content="width=device-width, initial-scale=1.0">
      <title>湖大电气院毕设轻松选</title>
      <style>
        body {{
          font-family: Arial, sans-serif;
          display: flex;
          padding: 20px;
        }}
        .info-container {{
          display: flex;
          flex-wrap: wrap;
          gap: 20px;
          justify-content: center;      /* 水平居中 */
          width: 100%;
        }}
        .info-item {{
          width: 45%;
          border: 1px solid #ddd;
          padding: 10px;
          border-radius: 5px;
          box-shadow: 0 0 5px rgba(0, 0, 0, 0.1);
          display: block;
        }}
        .info-item h3 {{
          margin: 0 0 10px 0;
          font-size: 18px;
        }}
        .info-container {
          display: flex;
          flex-wrap: wrap;
          justify-content: center;      /* 水平居中 */
          gap: 20px;
        }
        .info-item {
          width: 45%;
          border: 1px solid #ddd;
          padding: 10px;
          border-radius: 5px;
          box-shadow: 0 0 5px rgba(0, 0, 0, 0.1);
          display: block;
        }
        .info-item h3 {
          margin: 0 0 10px 0;
          font-size: 18px;
        }
        /* 修改 toggle-content 样式 */
        .toggle-content {
          visibility: hidden;
          opacity: 0;
          transform: scaleY(0);
          height: 0;
          transition: opacity 0.3s ease, visibility 0s 0.3s, transform 0.3s ease;
          transform-origin: top;
          white-space: pre-line;
        }
        
        .toggle-content.open {
          visibility: visible;
          opacity: 1;
          transform: scaleY(1);
          height: auto; /* 让内容自然展开 */
          transition: opacity 0.3s ease, visibility 0s 0s, transform 0.3s ease;
        }
        
        /* 修改 toggle-btn 样式，使按钮切换更加平滑 */
        .toggle-btn {
          cursor: pointer;
          color: #007BFF;
          transition: transform 0.2s ease;
        }
        /* 加载动画样式 */
        #loading {
          position: fixed;
          top: 50%;
          left: 50%;
          transform: translate(-50%, -50%);
          font-size: 24px;
          color: #007BFF;
          z-index: 9999;
        }
        #loading div {
          width: 50px;
          height: 50px;
          border: 5px solid #f3f3f3;
          border-top: 5px solid #3498db;
          border-radius: 50%;
          animation: spin 1s linear infinite;
        }
        @keyframes spin {
          0% { transform: rotate(0deg); }
          100% { transform: rotate(360deg); }
        }
        .search-bar {
          margin-bottom: 20px;
          display: flex;                /* 使用 flexbox 布局 */
          justify-content: center;      /* 水平居中 */
          align-items: center;          /* 垂直居中 */
        }
        .search-input {
          padding: 10px;
          width: 400px;
          margin-right: 10px;
          font-size: 16px;
        }
        .search-btn {
          padding: 10px 20px;
          background-color: #007BFF;
          color: white;
          border: none;
          cursor: pointer;
        }
        .direction-filter {
          display: flex;
          overflow-x: auto; /* 实现左右滑动 */
          padding: 10px 0;
          gap: 15px;
          white-space: nowrap;
          margin-left: 40px;  /* 左边距 */
          margin-right: 40px; /* 右边距 */
        }
        
        .direction-option {
          cursor: pointer;
          color: #007BFF;
          padding: 5px 10px;
          border-radius: 5px;
          transition: background-color 0.3s;
        }
        
        .direction-option:hover {
          background-color: #e6f7ff;
        }
        
        .direction-option.selected {
          background-color: #007BFF;
          color: white;
        }
      </style>
    </head>
    <body>
      
      <div id="loading">
        <div></div> <!-- 转圈加载动画 -->
        加载中...
      </div>
    
      <!-- 搜索框 -->
      <div class="search-bar">
        <input type="text" id="searchInput" class="search-input" placeholder="搜索感兴趣的毕设">
        <button class="search-btn" onclick="searchInfo()">搜索</button>
      </div>
      
      <!-- 搜索框下方添加复选框 -->
      <div class="search-bar">
        <label><input type="checkbox" id="fuzzySearch" checked> 模糊搜索 (所有字段)</label>
        <label><input type="checkbox" id="searchTitle"> 标题内容</label>
        <label><input type="checkbox" id="searchName"> 导师姓名</label>
        <label><input type="checkbox" id="searchTitleName"> 导师职称</label>
        <label><input type="checkbox" id="searchDirection"> 研究方向</label>
      </div>
    
      <!-- 新增研究方向筛选部分 -->
      <div class="direction-filter" id="directionFilter">
        <span class="direction-option" onclick="filterByDirection('所有')">所有 ({{totalProjects}})</span>
        <!-- 这里动态填充研究方向及其对应数量 -->
      </div>
    
      <div class="info-container" id="infoContainer">
    '''
    
    # 遍历info_list，生成每个导师信息的HTML
    for item in info_list:
        ktmc = item.get('ktmc', '未提供课程名称')
        jsxm = item.get('jsxm', '未提供导师姓名')
        dic_name1 = item.get('dic_name1', '未提供职称')
        email = item.get('email', '未提供联系邮箱')
        kbrssx = item.get('kbrssx', '未提供')
        xxrs = item.get('xxrs', 0)
        yxrs = item.get('yxrs', 0) if item.get('yxrs') is not None else 0
        yzrs = item.get('yzrs', 0)
        yjfx = item.get('yjfx', '未提供研究方向')
        mdyyq = item.get('mdyyq', '未提供目的与要求')
    
        # HTML模板
        html_content += f'''
        <div class="info-item" data-text="{ktmc} {jsxm} {dic_name1} {email} {kbrssx} {xxrs} {yxrs} {yzrs} {yjfx} {mdyyq}" data-direction="{yjfx}" teacher_name="{jsxm}" teacher_title="{dic_name1}">
          <h3>{ktmc}</h3>
          <p><strong>导师姓名:</strong> {jsxm}</p>
          <p><strong>导师职称:</strong> {dic_name1}</p>
          <p><strong>联系邮箱:</strong> {email}</p>
          <p><strong>可选人数上限:</strong> {kbrssx}</p>
          <p><strong>限选人数:</strong> {xxrs}</p>
          <p><strong>已选人数:</strong> {yxrs}</p>
          <p><strong>选中人数:</strong> {yzrs}</p>
          <p><strong>研究方向:</strong> {yjfx}</p>
    
          <!-- 展开与收起的目的与要求部分 -->
          <div class="toggle-btn" onclick="toggleContent('{item['bysj006id']}')">+</div>
          <div id="{item['bysj006id']}" class="toggle-content">{mdyyq}</div>
        </div>
        '''
    
    # 结束HTML结构
    html_content += '''
      </div>
    
      <script>
        // 切换展开与收起内容的函数
        function toggleContent(id) {
          var content = document.getElementById(id);
          var toggleButton = content.previousElementSibling;
        
          // 切换类名，减少DOM操作
          content.classList.toggle('open');  // 使用类切换控制展开和收回
        
          // 切换按钮内容
          if (content.classList.contains('open')) {
            toggleButton.innerHTML = "-";  // 展开时显示减号
          } else {
            toggleButton.innerHTML = "+";  // 收起时显示加号
          }
        }
    
        // 搜索功能
        function searchInfo() {
          var input = document.getElementById('searchInput').value.toLowerCase();
          var infoItems = document.getElementsByClassName('info-item');
        
          var fuzzySearch = document.getElementById('fuzzySearch').checked; // 判断是否选择了模糊搜索
          var searchTitle = document.getElementById('searchTitle').checked; // 判断是否选择了标题内容
          var searchName = document.getElementById('searchName').checked;   // 判断是否选择了导师姓名
          var searchTitleName = document.getElementById('searchTitleName').checked; // 判断是否选择了职称
          var searchDirection = document.getElementById('searchDirection').checked; // 判断是否选择了研究方向
        
          for (var i = 0; i < infoItems.length; i++) {
            var itemText = infoItems[i].getAttribute('data-text').toLowerCase();
            var title = infoItems[i].querySelector('h3').textContent.toLowerCase();
            var name = infoItems[i].getAttribute('teacher_name').toLowerCase();
            var titleName = infoItems[i].getAttribute('teacher_title').toLowerCase();
            var direction = infoItems[i].getAttribute('data-direction').toLowerCase();
        
            var match = false;
        
            if (fuzzySearch) {
              match = itemText.indexOf(input) > -1; // 模糊搜索
            } else {
              if (searchTitle && title.indexOf(input) > -1) match = true;
              if (searchName && name.indexOf(input) > -1) match = true;
              if (searchTitleName && titleName.indexOf(input) > -1) match = true;
              if (searchDirection && direction.indexOf(input) > -1) match = true;
            }
        
            if (match) {
              infoItems[i].style.display = 'block';  // 显示匹配的项目
            } else {
              infoItems[i].style.display = 'none';   // 隐藏不匹配的项目
            }
          }
        }
        
        // 统计所有项目的研究方向数量
        function generateDirectionFilter() {
          var directionCounts = {};
          var infoItems = document.getElementsByClassName('info-item');
      
          // 遍历所有项目，统计每个研究方向的数量
          for (var i = 0; i < infoItems.length; i++) {
            // 获取研究方向
            var directions = infoItems[i].getAttribute('data-direction');
            
            // 只有当研究方向存在且不为 null 时才执行
            if (directions && directions !== 'null' && directions.trim() !== '') {
              directions = directions.split(','); // 以逗号分割研究方向
              directions.forEach(function(direction) {
                direction = direction.trim(); // 去除空格
                directionCounts[direction] = (directionCounts[direction] || 0) + 1;
              });
            }
          }
    
          // 生成研究方向的 HTML 内容
          var directionFilter = document.getElementById('directionFilter');
          directionFilter.innerHTML = `<span class="direction-option" onclick="filterByDirection('所有')">所有 (${infoItems.length})</span>`;
        
          for (var direction in directionCounts) {
            var directionOption = document.createElement('span');
            directionOption.classList.add('direction-option');
            directionOption.textContent = `${direction} (${directionCounts[direction]})`;
            directionOption.setAttribute('data-direction', direction);
            directionOption.onclick = function() {
              filterByDirection(this.getAttribute('data-direction'));
            };
            directionFilter.appendChild(directionOption);
          }
        }
    
        // 根据选中的研究方向进行筛选
        function filterByDirection(direction) {
          var infoItems = document.getElementsByClassName('info-item');
          var selectedDirection = direction.toLowerCase();
      
          // 如果选择的是“所有”，则显示所有项目
          for (var i = 0; i < infoItems.length; i++) {
            var directions = infoItems[i].getAttribute('data-direction').toLowerCase();
            if (selectedDirection === '所有' || directions.indexOf(selectedDirection) > -1) {
              infoItems[i].style.display = 'block';
            } else {
              infoItems[i].style.display = 'none';
            }
          }
        
          // 更新选中的研究方向样式
          var directionOptions = document.getElementsByClassName('direction-option');
          for (var i = 0; i < directionOptions.length; i++) {
            if (directionOptions[i].textContent.indexOf(selectedDirection) > -1) {
              directionOptions[i].classList.add('selected');
            } else {
              directionOptions[i].classList.remove('selected');
            }
          }
        }
    
        // 页面加载完成后移除加载动画
        window.onload = function() {
          generateDirectionFilter();
          document.getElementById('loading').style.display = 'none';
        }
      </script>
    
    </body>
    </html>
    '''
    
    # 输出生成的HTML内容到文件
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print("HTML文件已生成！")
    
if __name__ == "__main__":
    authorization = input("请输入您的请求授权> ")
    data = getInfo(authorization)
    info_list = data['data']['list']['items']
    generate_HTML(info_list)