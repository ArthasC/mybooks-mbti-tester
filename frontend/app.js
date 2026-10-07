(function () {
  "use strict";

  var bridge = window.MyBooksToolBridge || null;
  var button = document.getElementById("start-button");
  var intro = document.getElementById("intro");
  var reading = document.getElementById("reading");
  var result = document.getElementById("result");
  var errorPanel = document.getElementById("error");
  var readingMessage = document.getElementById("reading-message");
  var errorMessage = document.getElementById("error-message");

  // 每种类型多条鉴定语，每次随机挑一条，“再占一次”也不会总看到同一句
  var quips = {
    ISTJ: [
      "你的书库井然有序，仿佛连书签都有自己的考勤表。",
      "阅读进度按时同步，书单按时清空，你就是书库界的守时模范。",
      "别人在书页里夹花瓣，你夹的是索引卡。"
    ],
    ISFJ: [
      "你把温柔夹进书页里，连朋友随口提过的那本书都记得惦记。",
      "你的书库总有一本，是专门留给“朋友说不定会需要”的。",
      "书库里的元数据被你补全的次数，比被你忽略的次数多得多。"
    ],
    INFJ: [
      "你读故事不只看结局，还会顺手推演整个人类的命运。",
      "半夜两点合上书，然后盯着天花板思考人生，是你的固定节目。",
      "你的书库像一座灯塔，只不过灯是调成了“忧郁蓝”。"
    ],
    INTJ: [
      "书单像一张战略地图，连下一本书都已经安排好了。",
      "你不是在读书，你是在为人生的下一阶段做尽职调查。",
      "待读清单排到了明年，而且有优先级和依赖关系。"
    ],
    ISTP: [
      "你喜欢拆解问题，也许书脊在你手里都像待研究样本。",
      "说明书你会读，教程你会跳着读，读完就想动手试试。",
      "书库里的实用类书籍，被打开次数最多的一定是带图的那几页。"
    ],
    ISFP: [
      "你的书库有审美，连沉默都选了最漂亮的那一本。",
      "买书先看封面，看完觉得内容配得上封面，就更开心了。",
      "你的阅读不赶进度，只赶心情，今天适合哪本，书会告诉你。"
    ],
    INFP: [
      "现实不够精彩时，你的书库负责开一扇通往别处的门。",
      "你和书里的角色聊得比和真人还多，而且他们从不打断你。",
      "合上书后要发呆十分钟，这是对作者最高的礼貌。"
    ],
    INTP: [
      "你不是想太多，只是每本书都能引出三条新问题。",
      "读到一半去查资料，查着查着就进了另一本书的兔子洞。",
      "你的书库没有分类法，只有一套只有你自己懂的“逻辑”。"
    ],
    ESTP: [
      "书还没看完，下一场冒险已经在你的愿望清单上。",
      "你读书的方式是：先翻到最刺激的那一章。",
      "比起坐着读，你更想把书里的事亲自干一遍。"
    ],
    ESFP: [
      "好故事就要有气氛，你的书库可能自带读书会音响。",
      "读到好句子会立刻念给身边人听，不听也要念。",
      "你的书库是派对现场，每一本都想拉出来聊两句。"
    ],
    ENFP: [
      "你的阅读路线像烟花：绚烂、跳跃，而且突然多出十本。",
      "同时在读七本书，每一本都说“这本也很重要”。",
      "书单上的每一本都是一个新世界，你全都想去，现在、立刻、马上。"
    ],
    ENTP: [
      "每个观点都值得聊聊——尤其是别人刚说完的那个。",
      "你读书是为了找漏洞，找到之后会开心地发一条长消息。",
      "书库里总有几本“我不同意但很有意思”的书，它们是你的最爱。"
    ],
    ESTJ: [
      "读书也要有进度，你的待读清单看起来像个项目计划。",
      "你有读书打卡表，而且连续打卡天数比健身卡还长。",
      "书库分类标注清晰，每本书都有自己的标签和位置，找起来一秒到位。"
    ],
    ESFJ: [
      "你会记住大家喜欢什么，也可能正准备给朋友组书单。",
      "你推荐的书，对方通常真的会看，因为你记得对方上次说过什么。",
      "书库里总有一本是“送给某某某”的预备礼物。"
    ],
    ENFJ: [
      "读到好东西就想分享，你的书库正在筹备一场共读活动。",
      "你的读后感常常变成一场温暖的演讲，听众还会鼓掌。",
      "你读书不只为自己，每读完一本都在想：这本适合推荐给谁？"
    ],
    ENTJ: [
      "目标明确、行动迅速：连阅读都像一个待完成的大项目。",
      "你读书的速度，让进度条都不好意思停下来。",
      "书库是你的作战室，每一本书都有它要完成的任务。"
    ]
  };

  // 有维度判断不出来时（出现 X），用这些话替代类型鉴定语
  var undecidedQuips = [
    "你的书库很有城府，线索藏得太深，占卜师暂时没看透。",
    "分类和标签留得太少了，书库目前只肯透露一部分的你。",
    "有的维度书库拒绝表态，大概在等你再多买几本。"
  ];

  // 每个维度的单字母吐槽，X 表示该维度票数持平
  var letterQuips = {
    E: "书库很热闹，像随时可以开一场读书会。",
    I: "书库很安静，每一本都像是只对你一个人说话。",
    S: "你偏爱看得见摸得着的内容，读完立刻就能用上。",
    N: "你的书库通往很多个世界，其中好几个并不在地图上。",
    T: "你读书习惯先找逻辑链，再决定要不要被感动。",
    F: "你读书先看感受，再决定要不要认同道理。",
    J: "你的书库有计划感，下一本通常已经想好了。",
    P: "你的书单随心情走，计划赶不上新书上架的速度。",
    X: "这个维度书库两边各投了一样多的票，暂时不肯站队。"
  };

  var dimensionTitles = ["能量", "感知", "判断", "生活"];

  function pick(list) {
    return list[Math.floor(Math.random() * list.length)];
  }

  function quipFor(profile) {
    if (profile.undecided && profile.undecided.length) return pick(undecidedQuips);
    var list = quips[profile.type];
    return list ? pick(list) : "你的书库还在认真思考怎么评价你。";
  }

  // 结合分类/标签的实际排名生成一两句“书库点评”，没有线索时返回空数组
  function shelfLines(profile) {
    var lines = [];
    var cat = (profile.top_categories || [])[0];
    var tag = (profile.top_tags || [])[0];
    var tail = (profile.top_tags || []).length > 1 ?
      (profile.top_tags || []).slice(-1)[0] : null;
    if (cat) {
      lines.push("「" + cat.name + "」以 " + cat.count + " 本稳居分类榜首，大概是你的本命区。");
    }
    if (tag) {
      lines.push("标签「" + tag.name + "」出现了 " + tag.count + " 次，书库里的暗号就是它。");
    }
    if (tail && tag && tail.name !== tag.name && tail.count < tag.count) {
      lines.push("「" + tail.name + "」也混进了高频榜，大概是你偶尔想换换口味的证据。");
    }
    var ratio = profile.book_count ? profile.books_with_clues / profile.book_count : 0;
    if (profile.book_count >= 10 && ratio < 0.5) {
      lines.push("有一半以上的书没贴分类或标签，占卜师只能隔着书脊猜。");
    }
    return lines;
  }

  function dimensionLines(dimensions) {
    return dimensions.map(function (item, index) {
      var letter = item.selected;
      return '<li><b>' + dimensionTitles[index] + ' · ' + escapeHtml(letter) + '</b>' +
        escapeHtml(letterQuips[letter] || "") + '</li>';
    });
  }

  var messages = [
    "第一步：请书库放下矜持……",
    "第二步：正在盘点你的精神零食……",
    "第三步：把标签排成星象图……",
    "最后一步：让书脊举手表决……"
  ];
  var messageTimer;

  function setTheme(theme) {
    document.body.setAttribute("data-theme", theme || "light");
  }

  function renderChips(items) {
    if (!items.length) return '<p class="empty">书库还没留下明显线索。</p>';
    return items.map(function (item) {
      return '<span class="chip">' + escapeHtml(item.name) +
        '<b>' + item.count + '</b></span>';
    }).join("");
  }

  function renderDimensions(dimensions) {
    return dimensions.map(function (item) {
      var left = item.left_percent;
      var right = item.right_percent;
      return '<div class="dimension">' +
        '<div class="dimension-head"><span>' + escapeHtml(item.left_name) +
        ' <strong>' + item.left + ' ' + item.left_count + '</strong></span>' +
        '<span class="dimension-label">' + escapeHtml(item.right_name) +
        ' <strong>' + item.right_count + ' ' + item.right + '</strong></span></div>' +
        '<div class="dimension-track" aria-label="' + escapeHtml(item.left_name) +
        ' ' + left + '%，' + escapeHtml(item.right_name) + ' ' + right + '%">' +
        '<span class="dimension-left" style="width:' + left + '%"></span>' +
        '<span class="dimension-right" style="width:' + right + '%"></span></div>' +
        '<div class="dimension-caption"><span>' + item.left + ' 线索 ' + left +
        '%</span><span>' + item.right + ' 线索 ' + right + '%</span></div></div>';
    }).join("");
  }

  function renderProfile(profile) {
    if (!profile.book_count) {
      result.innerHTML = '<section class="result-card"><div class="eyebrow">书库目前一片空白</div>' +
        '<h2>占卜师没有可翻的书。</h2><p class="result-quip">先放几本书进书库，再来看看你的书库会怎么评价你。</p></section>' +
        '<div class="result-actions"><span class="confidence">本次没有读取到书籍。</span>' +
        '<button class="start-button retry-button" id="again-button">重来一次 <span>↗</span></button></div>';
      document.getElementById("again-button").addEventListener("click", start);
      return;
    }

    var clueNote = profile.books_with_clues ?
      "在 " + profile.books_with_clues + " 本带有分类或标签的书里，" :
      "书库暂时没贴分类或标签；这次结果属于纯随机玄学，";
    var topCategories = profile.top_categories || [];
    var topTags = profile.top_tags || [];
    result.innerHTML =
      '<section class="result-card">' +
        '<div class="result-heading"><div><div class="eyebrow">书库鉴定结果 · 一本正经 · 严肃认真</div>' +
        '<h2>' + escapeHtml(profile.type || "????") + '</h2><h3>' +
        escapeHtml(profile.type_name || "待书库补充线索") + '</h3></div>' +
        '<div class="seal">书库认证<br>有理有据<br>但不多</div></div>' +
        '<p class="result-quip">' + escapeHtml(quipFor(profile)) +
        '</p><div class="stats">' +
          '<div class="stat"><strong>' + profile.book_count + '</strong><span>本藏书</span></div>' +
          '<div class="stat"><strong>' + profile.category_count + '</strong><span>种分类线索</span></div>' +
          '<div class="stat"><strong>' + profile.tag_count + '</strong><span>种标签线索</span></div>' +
        '</div><div class="dimensions">' + renderDimensions(profile.dimensions) + '</div>' +
      '</section>' +
      '<section class="result-card"><h3>书库碎碎念</h3><ul class="roast-list">' +
        dimensionLines(profile.dimensions).concat(shelfLines(profile).map(function (line) {
          return '<li class="shelf-line">' + escapeHtml(line) + '</li>';
        })).join("") + '</ul></section>' +
      '<section class="result-card sample">' +
        '<div><h3>最常出现的分类</h3><div class="chip-list">' + renderChips(topCategories) + '</div></div>' +
        '<div><h3>书库高频暗号</h3><div class="chip-list">' + renderChips(topTags) + '</div></div>' +
      '</section>' +
      '<section class="result-card"><p class="verdict-note">' +
        escapeHtml(clueNote + "每本书最多为每条人格维度投一票，左右票数相同的维度记为 X。MBTI 类型由书籍分类与标签中的关键词推测，" +
        "与正式心理测验无关，也不能代表真实人格。" + profile.confidence + "。") +
      '</p></section>' +
      '<div class="result-actions"><span class="confidence">' + escapeHtml(profile.confidence) +
        ' · 纯属娱乐，请勿拿去面试。</span><button class="start-button retry-button" id="again-button">' +
        '重来一次 <span>↗</span></button></div>';
    document.getElementById("again-button").addEventListener("click", start);
  }

  function escapeHtml(value) {
    return String(value).replace(/[&<>"']/g, function (char) {
      return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[char];
    });
  }

  function fetchProfile() {
    if (bridge && typeof bridge.fetch === "function") {
      return bridge.fetch("analyze", { method: "GET" });
    }
    return fetch("/api/toolbox/tool/mbti_tester/analyze", { credentials: "same-origin" })
      .then(function (response) {
        if (!response.ok) throw new Error("读取书库失败（HTTP " + response.status + "）。");
        return response.json();
      });
  }

  function start() {
    window.clearInterval(messageTimer);
    intro.hidden = true;
    result.hidden = true;
    errorPanel.hidden = true;
    reading.hidden = false;
    var index = 0;
    readingMessage.textContent = messages[index];
    messageTimer = window.setInterval(function () {
      index = (index + 1) % messages.length;
      readingMessage.textContent = messages[index];
    }, 900);

    fetchProfile().then(function (response) {
      if (!response || response.err !== "ok" || !response.data) {
        throw new Error((response && response.msg) || "服务暂时没有返回有效结果，请稍后重试。");
      }
      window.clearInterval(messageTimer);
      renderProfile(response.data);
      reading.hidden = true;
      result.hidden = false;
    }).catch(function (error) {
      window.clearInterval(messageTimer);
      reading.hidden = true;
      errorMessage.textContent = error && error.message ? error.message : "读取书库时发生未知错误。";
      errorPanel.hidden = false;
    });
  }

  button.addEventListener("click", start);
  document.getElementById("retry-button").addEventListener("click", start);
  if (bridge) {
    setTheme(bridge.theme);
    if (typeof bridge.onThemeChange === "function") bridge.onThemeChange(setTheme);
  }
})();
