#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""第二批：再生成 10 篇 GEO/SEO 文章（问答体 + E-E-A-T + JSON-LD），并自动接入 sitemap 与文章列表页。"""
import json, os, html

OUT = "/Users/a123456/WorkBuddy/2026-08-11-00-08-08/site/articles"
SITEMAP = "/Users/a123456/WorkBuddy/2026-08-11-00-08-08/site/sitemap.xml"
INDEX = "/Users/a123456/WorkBuddy/2026-08-11-00-08-08/site/articles/index.html"
SITE = "https://www.ryrise.cn"
TODAY = "2026-08-11"

# 全站统一的 CTA / 页脚 / 微信弹窗 / 百度自动推送（与现有文章完全一致）
TAIL = '''
    <section class="cta site-contact" id="contact">
    <div class="container cta__inner">
      <h2>想看看你的账号问题出在哪？</h2>
      <p>留个信息，我先免费帮你把账号诊断一遍，有用你再考虑合作。提交后我们会收到邮件，主动联系你。</p>
      <form class="site-contact-form" onsubmit="return false;">
        <div class="row">
          <input type="text" name="name" placeholder="你的称呼 / 工厂名称" required />
          <input type="text" name="contact" placeholder="微信或手机号" required />
        </div>
        <input type="text" name="industry" placeholder="行业（如：五金 / 机械 / 包装）" />
        <textarea name="pain" rows="3" placeholder="一句话说下你现在的获客卡点"></textarea>
        <button type="submit" class="btn btn--primary btn--lg">提交，免费诊断我的账号</button>
      </form>
      <p class="cta__note">或直接加微信「小赖还不赖」/ 手机 15112850612，把抖音号发我，24 小时内出诊断结论。</p>
    </div>
  </section>
  <footer class="footer">
    <div class="container footer__inner">
      <div class="footer__brand">
        <img src="../images/brand-visual.png" alt="若云科技品牌视觉" class="footer__logo" />
        <div>
          <div class="footer__name">东莞市若云科技有限公司</div>
          <div class="footer__sub">工厂抖音获客代运营 · GEO 让 AI 也推荐你</div>
        </div>
      </div>
      <div class="footer__links">
        <a href="../index.html">首页</a>
        <a href="../company.html">公司</a>
        <a href="../cases.html">案例</a>
        <a href="../pricing.html">价格</a>
        <a href="../news.html">资讯</a>
        <a href="../articles/index.html">文章</a>
      </div>
      <div class="footer__contact">
        <div>微信 / 手机：15112850612</div>
        <div>抖音：小赖还不赖</div>
        <div>邮箱：<a href="mailto:297388441@qq.com">297388441@qq.com</a></div>
      </div>
      <div class="footer__copy">© <span id="year"></span> 东莞市若云科技有限公司（抖音「小赖还不赖」运营主体）</div>
    </div>
  </footer>
  <script src="../script.js"></script>
  <!-- 微信二维码弹窗 -->
  <div class="qr-modal" id="wechatModal" aria-hidden="true">
    <div class="qr-modal__mask" data-close></div>
    <div class="qr-modal__box">
      <button class="qr-modal__close" data-close aria-label="关闭">×</button>
      <div class="qr-modal__title">扫码联系我</div>
      <div class="qr-modal__name">小赖还不赖</div>
      <div class="qr-modal__qrs">
  <div class="qr-modal__qr"><img src="../images/wechat-qr.jpg" alt="微信二维码：小赖还不赖" /><span>微信：小赖还不赖</span></div>
  <div class="qr-modal__qr"><img src="../images/douyin-qr.jpg" alt="抖音二维码：小赖还不赖" /><span>抖音：小赖还不赖</span></div>
</div>
      <p class="qr-modal__tip">加我微信，把抖音号发我，24 小时内给你一份免费账号诊断。</p>
      <p class="qr-modal__alt">手机 / 微信同号：15112850612</p>
    </div>
  </div>

  <!-- Baidu auto-push (普通收录-自动推送): 访客访问即自动提交当前URL, 不占API配额 -->
  <script>
  (function(){
      var bp = document.createElement('script');
      var curProtocol = window.location.protocol.split(':')[0];
      if (curProtocol === 'https') {
          bp.src = 'https://zz.bdstatic.com/linksubmit/push.js';
      } else {
          bp.src = 'http://push.zhanzhang.baidu.com/push.js';
      }
      var s = document.getElementsByTagName("script")[0];
      s.parentNode.insertBefore(bp, s);
  })();
  </script>
</body>
</html>
'''

NAV = '''  <header class="nav" id="nav">
  <div class="container nav__inner">
    <a href="../index.html" class="nav__logo">若云<span>科技</span></a>
    <button class="nav__toggle" id="navToggle" aria-label="打开菜单" aria-expanded="false"><span></span><span></span><span></span></button>
    <nav class="nav__menu" id="navMenu" aria-label="主导航">
      <a href="../index.html">首页</a>
      <a href="../company.html">公司</a>
      <a href="../cases.html">案例</a>
      <a href="../pricing.html">价格</a>
      <a href="../news.html">资讯</a>
      <a href="../articles/index.html">文章</a>
      <a data-wechat class="nav__cta">联系我</a>
    </nav>
  </div>
</header>
'''

def render_section(sec):
    kind = sec[0]
    if kind == "h2":
        return f"        <h2>{sec[1]}</h2>\n"
    if kind == "p":
        return f"        <p>{sec[1]}</p>\n"
    if kind == "ul":
        items = "\n".join(f"          <li>{it}</li>" for it in sec[1])
        return f"        <ul>\n{items}\n        </ul>\n"
    if kind == "callout":
        return f'        <div class="callout">\n          {sec[1]}\n        </div>\n'
    raise ValueError(kind)

def render_article(a):
    slug = a["slug"]
    url = f"{SITE}/articles/{slug}"
    faq_json = {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {"@type": "Question", "name": q["q"],
             "acceptedAnswer": {"@type": "Answer", "text": q["a"]}}
            for q in a["faq"]
        ],
    }
    article_json = {
        "@context": "https://schema.org",
        "@type": "Article",
        "headline": a["title"],
        "author": {"@type": "Person", "name": "赖先生"},
        "publisher": {"@type": "Organization", "name": "东莞市若云科技有限公司"},
        "about": a["about"],
    }
    body = "".join(render_section(s) for s in a["sections"])
    faq_html = "".join(
        f'          <div class="faq__item">\n            <h3>{q["q"]}</h3>\n            <p>{q["a"]}</p>\n          </div>\n'
        for q in a["faq"]
    )
    related_html = "".join(
        f'          <a href="{r["href"]}">{r["title"]}</a>\n' for r in a["related"]
    )
    doc = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>{a["title"]}</title>
  <meta name="description" content="{a["desc"]}" />
  <link rel="stylesheet" href="../styles.css" />
  <script type="application/ld+json">
  {json.dumps(article_json, ensure_ascii=False, indent=2)}
  </script>
<link rel="canonical" href="{url}" />
<meta property="og:type" content="website" />
<meta property="og:title" content="{a["title"]}" />
<meta property="og:description" content="{a["desc"]}" />
<meta property="og:url" content="{url}" />
<meta property="og:image" content="{SITE}/images/brand-visual.png" />
<meta property="og:site_name" content="若云科技" />
  <script type="application/ld+json">
  {json.dumps(faq_json, ensure_ascii=False, indent=2)}
  </script>
</head>
<body>
{NAV}
  <article class="post">
    <div class="container">
      <div class="post__hero">
        <p class="breadcrumb"><a href="../index.html">首页</a> / <a href="index.html">文章</a> / {a["cat_label"]}</p>
        <p class="post__cat">{a["category"]}</p>
        <h1 class="post__title">{a["title"]}</h1>
        <p class="post__lead">{a["lead"]}</p>
      </div>

      <div class="post__body">
{body}        <div class="faq">
          <h2>关于「{a["cat_label"]}」的快速问答</h2>
{faq_html}        </div>

        <div class="related">
          <h3>相关阅读</h3>
{related_html}        </div>
      </div>
    </div>
  </article>
{TAIL}'''
    return doc

ARTICLES = [
{
  "slug": "dou-yin-suan-fa",
  "title": "抖音推荐机制是怎么回事？工厂内容怎么顺着来",
  "desc": "不用懂代码，只要懂系统想把什么推给谁。讲清完播、互动、标签三件事，工厂内容怎么顺着算法拿到客资。",
  "category": "算法 · 信息类",
  "cat_label": "算法",
  "about": "抖音推荐机制",
  "card_meta": "算法 · 信息类",
  "card_desc": "完播、互动、标签——三件事决定推不推你。",
  "lead": "不用懂代码，只要懂「系统想把什么内容推给谁」。讲清完播、互动、标签三件事，工厂内容怎么顺着来拿客资。",
  "sections": [
    ("h2", "抖音靠什么决定推不推你的视频"),
    ("p", "核心指标是完播率、互动率（点赞、评论、转发、收藏），以及内容被分到的标签准不准。系统先把视频推给一小批「可能感兴趣」的人，数据好就往更大流量池推。"),
    ("h2", "完播率：前 3 秒和「钩子」决定生死"),
    ("p", "工厂视频最该改的就是开头。别铺垫，直接戳痛点或抛反常识，让人想看完。开头留不住人，后面再好也白搭。"),
    ("h2", "互动率：让同行老板「有话想说」"),
    ("p", "提问、站队、晒证据引发讨论，比漂亮话有用。B 端用户在评论区问问题，本身就是客资信号，比单纯播放量更有价值。"),
    ("h2", "标签：你持续讲什么，系统就认你是「哪类号」"),
    ("p", "垂直、稳定地讲工厂相关内容，标签越准，推的人越对。今天讲段子明天讲干货，系统不知道推给谁，流量就散了。"),
    ("callout", "<strong>核心：</strong>完播看开头、互动看话题、标签看坚持。工厂内容不用追热点，把「专业 + 真实」做稳，系统自然把你推给对的人。"),
  ],
  "faq": [
    {"q": "投流能绕过算法吗？", "a": "投流是放大，不是替代。内容本身数据差，投流也救不回来，钱花得冤。先打磨内容，再考虑投。"},
    {"q": "一条视频要多少完播才算好？", "a": "没有统一线，看同行基准。工厂类账号完播能到 20%-30% 算健康，重点是逐条比自己上一期好。"},
  ],
  "related": [
    {"href": "wei-shen-me-nan-zuo.html", "title": "制造业短视频，为什么多数工厂做不起来？"},
    {"href": "gong-chang-duan-shi-pin-jie-gou.html", "title": "工厂短视频脚本怎么写结构？B 端 5 段式模板"},
    {"href": "cong-0-dao-1.html", "title": "工厂抖音账号从 0 到 1 怎么起？"},
  ],
},
{
  "slug": "shi-pin-hao-gong-huo",
  "title": "视频号工厂获客怎么做？微信生态的被动流量",
  "desc": "视频号背靠微信，客户刷到就能顺手加你、转发给同事。工厂怎么用最低成本吃这波被动流量、做信任获客。",
  "category": "平台获客 · 视频号",
  "cat_label": "视频号",
  "about": "视频号工厂获客",
  "card_meta": "平台获客 · 视频号",
  "card_desc": "微信生态的信任链，做被动获客最省力。",
  "lead": "视频号背靠微信，客户刷到就能顺手加你、转发给同事。工厂怎么用最低成本吃这波被动流量，把信任做扎实。",
  "sections": [
    ("h2", "视频号的特殊之处：熟人 + 算法混推"),
    ("p", "视频号会推给微信好友和好友的好友，也能被算法发现。一条被客户转发到群里，等于免费精准触达一整批同行。"),
    ("h2", "内容怎么适配视频号用户"),
    ("p", "视频号用户偏成熟、偏决策层。讲行业判断、避坑、成本逻辑，比花哨剧情更对味。他们来这里是找「靠谱的判断」，不是找乐子。"),
    ("h2", "承接要顺着微信来"),
    ("p", "视频号天然接微信生态。主页留企业微信、评论区引导私信、直播挂预约，路径比跨平台短得多，加了就能聊。"),
    ("h2", "和抖音怎么分工"),
    ("p", "抖音拿主动搜索和曝光，视频号拿微信里的信任和转发。两条线内容可复用，渠道互补，不必二选一。"),
    ("callout", "<strong>视频号不是「再发一遍抖音」</strong>，是利用微信的信任链做被动获客。内容讲判断、承接走微信，是最省力的打法。"),
  ],
  "faq": [
    {"q": "视频号需要投流吗？", "a": "起步不用。先把内容做对、靠转发和搜索自然跑，有稳定客资再考虑投。"},
    {"q": "工厂适合视频号吗？", "a": "适合决策周期长、靠信任成交的品类，尤其设备、原材料、定制加工这类。"},
  ],
  "related": [
    {"href": "dou-yin-vs-baidu.html", "title": "抖音搜索和百度搜索，工厂获客区别在哪？"},
    {"href": "geo-vs-dou-yin-sou-suo.html", "title": "GEO 和抖音搜索流，工厂怎么双联动吃流量？"},
    {"href": "dai-yun-ying-bi-keng.html", "title": "找工厂代运营怎么避坑？5 条硬标准筛掉不靠谱的"},
  ],
},
{
  "slug": "xiao-hong-shu-gong-huo",
  "title": "小红书工厂获客怎么做？B2B 也能种草",
  "desc": "别以为小红书只卖美妆。采购、创业者、小老板都在上面搜「工厂」「源头」「代工」。工厂怎么用笔记吃到搜索流量。",
  "category": "平台获客 · 小红书",
  "cat_label": "小红书",
  "about": "小红书工厂获客",
  "card_meta": "平台获客 · 小红书",
  "card_desc": "搜索拦截 + 信任种草，B2B 也能做。",
  "lead": "别以为小红书只卖美妆。采购、创业者、小老板都在上面搜「工厂」「源头」「代工」。工厂怎么用笔记吃到搜索流量。",
  "sections": [
    ("h2", "小红书的流量逻辑：搜索 + 种草"),
    ("p", "大量用户带着需求搜「XX 源头工厂」「怎么找代工」。笔记排在前面，等于守在客户搜索路口，被动等客上门。"),
    ("h2", "工厂笔记写什么才不像广告"),
    ("p", "用「帮用户避坑」「科普选型」「晒车间真实样」的语气，少说「我家最好」，多给方法。平台厌广，硬广会被限流。"),
    ("h2", "关键词要埋进标题和正文"),
    ("p", "把「源头工厂」「代工」「东莞」「小批量」这类真实搜词自然写进标题和前几句，机器才好理解、推给对的人。"),
    ("h2", "承接走私信，别急着卖"),
    ("p", "小红书适合先建信任再引流。评论区、私信给价值，再导流到微信做深度转化，急不得。"),
    ("callout", "<strong>小红书对工厂的价值是「搜索拦截 + 信任种草」。</strong>内容做科普避坑、词埋自然，比硬广走得远。"),
  ],
  "faq": [
    {"q": "工厂在小红书能直接成交吗？", "a": "少。更适合做线索和信任，最后引流到微信、官网深度谈。"},
    {"q": "没团队能做吗？", "a": "能。每周 2-3 篇笔记，图文即可，重点是持续和关键词对。"},
  ],
  "related": [
    {"href": "sou-suo-liu-liang.html", "title": "工厂抖音怎么做搜索流量？搜索流布局实操"},
    {"href": "dou-yin-sou-suo-liu-chi-fa.html", "title": "工厂抖音搜索流怎么吃透？从搜词布局到内容承接"},
    {"href": "di-yu-dai-yun-ying.html", "title": "地域代运营怎么选？本地工厂获客的坑"},
  ],
},
{
  "slug": "bai-du-ai-cai-gou",
  "title": "百度爱采购 vs 抖音获客，工厂怎么选？",
  "desc": "一个守搜索、一个做内容。工厂预算有限，先搞懂两者差别，别把钱和精力撒错地方，按品类选渠道。",
  "category": "渠道对比 · 百度爱采购",
  "cat_label": "渠道对比",
  "about": "百度爱采购vs抖音",
  "card_meta": "渠道对比 · 爱采购",
  "card_desc": "守搜索 vs 做内容，按品类选。",
  "lead": "一个守搜索、一个做内容。工厂预算有限，先搞懂两者差别，别把钱和精力撒错地方，按品类选渠道才稳。",
  "sections": [
    ("h2", "百度爱采购：守在「主动搜」的路口"),
    ("p", "客户搜「XX 厂家」「批发」，爱采购把你的店推出来。适合标品、强搜索意图的品类，按效果付费，客户带着订单来。"),
    ("h2", "抖音获客：用内容和人设养信任"),
    ("p", "抖音不靠搜，靠刷。老板 IP、车间实拍、行业干货，把「这家厂可信」种进客户脑子，带来长期客资。"),
    ("h2", "三个维度帮你想清楚"),
    ("ul", [
      "决策方式：客户是「搜」还是「刷」",
      "品类属性：标品重搜索、非标/定制重信任",
      "团队资源：开店运营 vs 持续出内容",
    ]),
    ("h2", "怎么搭配最稳"),
    ("p", "标品厂爱采购先吃搜索；非标、定制厂抖音做信任更划算。有能力的厂两条线都布，搜索截流 + 内容养客。"),
    ("callout", "<strong>爱采购是「客户找你时在场」，抖音是「客户没想找时也记住你」。</strong>标品先爱采购，非标先抖音，能者双线。"),
  ],
  "faq": [
    {"q": "小厂先上爱采购还是先做抖音？", "a": "看品类。标品、客单价低、强搜索的，爱采购见效快；非标、靠信任成交的，抖音更值得长期投入。"},
    {"q": "两个都要花钱吗？", "a": "爱采购有入驻和点击成本；抖音起步靠内容，人力为主。都可先小投入测效果。"},
  ],
  "related": [
    {"href": "dou-yin-vs-baidu.html", "title": "抖音搜索和百度搜索，工厂获客区别在哪？"},
    {"href": "geo-vs-seo.html", "title": "GEO 和 SEO，工厂应该先做哪个？"},
    {"href": "dai-yun-ying-duo-shao-qian.html", "title": "工厂代运营多少钱？价格构成拆解"},
  ],
},
{
  "slug": "kou-bo-jiao-ben-xie-fa",
  "title": "工厂短视频口播脚本怎么写？给一套可套模板",
  "desc": "别从空白页开始。给你一套「钩子—立场—证据—方法—收口」口播模板，照着填就能拍，新手也不空。",
  "category": "短视频 · 口播脚本",
  "cat_label": "口播脚本",
  "about": "工厂口播脚本写法",
  "card_meta": "操作 · 口播脚本",
  "card_desc": "钩子—立场—证据—方法—收口，照填就能拍。",
  "lead": "别从空白页开始。给你一套「钩子—立场—证据—方法—收口」口播模板，照着填就能拍，新手也不空。",
  "sections": [
    ("h2", "先写「一句话钩子」，不是写开头"),
    ("p", "钩子是整条视频的钩。先想清楚：这条要解决客户哪个具体疑问或痛点，用一句话戳中。例：「你家的五金件交期是不是总拖？」"),
    ("h2", "立场 + 证据，构成信任两段"),
    ("p", "钩子之后，一句话站队（我站在客户这边），马上接真实证据（车间、检测、参数）。B 端信眼见为实，空话没用。"),
    ("h2", "给方法，让客户「记住你专业」"),
    ("p", "把经验变成客户能用的标准或清单，比如「选冲压厂看 3 个参数」。给方法 = 立专业，客户才会记住你。"),
    ("h2", "收口给动作，别戛然而止"),
    ("p", "结尾明确下一步：加微信领清单、看官网流程。没收口，流量就散了，前面白拍。"),
    ("callout", "<strong>口播模板：一句话钩子 → 立场 → 证据 → 给方法 → 收口。</strong>先套满练手感，熟了再灵活调整。"),
  ],
  "faq": [
    {"q": "要写逐字稿还是列要点？", "a": "新手建议逐字稿，关键信息（参数、标准、收口）必须固定，别临场丢重点。"},
    {"q": "一条口播多久合适？", "a": "工厂干货 30-60 秒最稳，讲清一个点比贪多强。"},
  ],
  "related": [
    {"href": "gong-chang-duan-shi-pin-jie-gou.html", "title": "工厂短视频脚本怎么写结构？B 端 5 段式模板"},
    {"href": "shi-pin.html", "title": "工厂短视频怎么拍才不像自嗨？"},
    {"href": "cong-0-dao-1.html", "title": "工厂抖音账号从 0 到 1 怎么起？"},
  ],
},
{
  "slug": "shu-zi-ren-zhu-bo",
  "title": "数字人/AI 主播 vs 真人出镜，工厂怎么选？",
  "desc": "数字人便宜能量产，真人贵但可信。工厂获客到底用哪个？讲清各自适合的场景，别盲目跟风，还要注意合规。",
  "category": "出镜形式 · 数字人",
  "cat_label": "数字人",
  "about": "数字人主播vs真人",
  "card_meta": "出镜形式 · 数字人",
  "card_desc": "数字人做量、真人做信任，合规标注。",
  "lead": "数字人便宜能量产，真人贵但可信。工厂获客到底用哪个？讲清各自适合的场景，别盲目跟风，还要注意合规。",
  "sections": [
    ("h2", "数字人的优势与天花板"),
    ("p", "成本低、能 7×24 量产、不挑状态。但 B 端客户买的是「真实可靠」，数字人难传递车间实感和人格信任，容易显得「假」。"),
    ("h2", "真人出镜的不可替代性"),
    ("p", "老板、师傅真人讲，车间实拍，信任锚最扎实。B 端高客单、长决策，真人信任转化明显更稳，这是数字人给不了的。"),
    ("h2", "怎么组合最划算"),
    ("p", "数字人做 repetitive 的资讯播报、答疑类量产内容；真人只出关键信任内容（工艺、案例、观点）。把真人用在刀刃上。"),
    ("h2", "合规提醒"),
    ("p", "用数字人要明确标注，别冒充真人误导客户。平台对「拟真人」有标注要求，违规会被限流甚至下架，得不偿失。"),
    ("callout", "<strong>数字人做量、真人做信任。</strong>关键信任内容必须真人，数字人仅做辅助播报，且要合规标注。"),
  ],
  "faq": [
    {"q": "数字人能替代老板 IP 吗？", "a": "不能替代信任。可做辅助内容，但老板真人出镜的信任价值数字人给不了。"},
    {"q": "用数字人会违规吗？", "a": "只要不冒充真人、按要求标注，一般合规；冒充或误导就有风险。"},
  ],
  "related": [
    {"href": "wei-shen-me-lao-ban-ip.html", "title": "工厂为什么一定要做老板 IP？"},
    {"href": "gong-chang-lao-ban-ip-ren-she.html", "title": "工厂老板 IP 人设怎么定？4 步找准出镜定位"},
    {"href": "shi-pin.html", "title": "工厂短视频怎么拍才不像自嗨？"},
  ],
},
{
  "slug": "gong-chang-wang-zhan-huo-ke",
  "title": "工厂企业官网怎么帮获客？别只当门面",
  "desc": "很多工厂官网只是「门面」。其实官网是信任背书 + 搜索入口 + GEO 信源的三合一。怎么把官网真正用起来获客。",
  "category": "官网获客 · 信息类",
  "cat_label": "官网获客",
  "about": "工厂官网获客",
  "card_meta": "信息 · 官网获客",
  "card_desc": "信任背书 + 搜索入口 + GEO 信源三合一。",
  "lead": "很多工厂官网只是「门面」。其实官网是信任背书 + 搜索入口 + GEO 信源的三合一。怎么把官网真正用起来获客。",
  "sections": [
    ("h2", "官网是「信任背书」的终极载体"),
    ("p", "客户货比三家时，一个专业、信息完整、能查到的官网，比十句口头承诺都管用。公司、案例、资质、联系方式齐全，信任立刻不一样。"),
    ("h2", "官网是搜索和 GEO 的「信源」"),
    ("p", "百度、抖音搜你名字，官网排前面最稳。AI 回答「推荐 XX 厂」时，也优先抓官网这类权威信源。官网内容结构化，被收录、被引用都更顺。"),
    ("h2", "官网要放什么才获客"),
    ("ul", [
      "清晰的业务与产品介绍",
      "真实案例与客户反馈",
      "资质证书与联系方式",
      "明确的留资入口 + FAQ 与行业文章",
    ]),
    ("h2", "和抖音怎么配合"),
    ("p", "抖音负责「刷到认识你」，官网负责「深入了解并信任你」。视频里引导看官网，官网承接详情和留资，闭环就通了。"),
    ("callout", "<strong>官网不是门面，是信任 + 搜索入口 + GEO 信源的三合一。</strong>信息全、可查、可留资，才真正帮获客。"),
  ],
  "faq": [
    {"q": "小厂有必要做官网吗？", "a": "有。哪怕简单页，也是信任和搜索的基本盘，尤其被 AI 推荐时官网权重高。"},
    {"q": "官网和抖音冲突吗？", "a": "不冲突，互补。抖音拉新认识，官网承接深度信任。"},
  ],
  "related": [
    {"href": "geo-shi-me-shi.html", "title": "GEO 是什么？怎么让豆包、DeepSeek 推荐你的工厂"},
    {"href": "geo-zen-me-zuo.html", "title": "GEO 怎么做？工厂落地「让 AI 推荐你」的 5 步"},
    {"href": "dai-yun-ying-bi-keng.html", "title": "找工厂代运营怎么避坑？5 条硬标准筛掉不靠谱的"},
  ],
},
{
  "slug": "si-yu-cheng-jie",
  "title": "抖音引流到微信后怎么承接？私域不浪费",
  "desc": "把人引到微信只是开始。接不住、聊不动，流量全漏。讲清从「加好友」到「成交」的承接三步，私域不浪费。",
  "category": "私域承接 · 操作类",
  "cat_label": "私域承接",
  "about": "抖音引流微信承接",
  "card_meta": "操作 · 私域承接",
  "card_desc": "加好友后怎么接住、养熟、不漏单。",
  "lead": "把人引到微信只是开始。接不住、聊不动，流量全漏。讲清从「加好友」到「成交」的承接三步，私域不浪费。",
  "sections": [
    ("h2", "第一步：加好友后的「第一句话」"),
    ("p", "别发广告。先确认需求、给一点即时价值（如诊断结论、清单），让客户觉得「加对了」，信任从第一句开始。"),
    ("h2", "第二步：用标签把客户分层"),
    ("p", "按行业、需求、意向给微信好友打标签，后续发的内容才精准，不扰民也不漏单。分层是私域的基本功。"),
    ("h2", "第三步：持续给价值，等成交"),
    ("p", "B 端决策慢。定期发行业判断、案例、避坑，保持专业存在感。客户有需求时第一个想到你，而不是别人。"),
    ("h2", "别踩的坑"),
    ("p", "一上来硬推、朋友圈刷屏、不回消息，都会把刚加的客户推走。承接是「养」，不是「收割」。"),
    ("callout", "<strong>承接三步：第一句给价值 → 标签分层 → 持续养。</strong>抖音引来的人，靠微信里「专业且不过度」的承接留住。"),
  ],
  "faq": [
    {"q": "微信好友多久跟进一次？", "a": "看意向。高意向当天跟进，普通的一周一次轻触达，别骚扰。"},
    {"q": "一个人能接住多少客户？", "a": "初期几十个靠标签和模板够用；量上来要用 SOP 和工具，别全靠脑子记。"},
  ],
  "related": [
    {"href": "si-xin-hua-shu.html", "title": "抖音私信话术怎么写？客户主动问时这样接"},
    {"href": "you-bo-fang-mei-ke-hu.html", "title": "有播放没客户？工厂短视频流量变客资的断点"},
    {"href": "dai-yun-ying-bi-keng.html", "title": "找工厂代运营怎么避坑？5 条硬标准筛掉不靠谱的"},
  ],
},
{
  "slug": "nei-rong-chi-xu",
  "title": "工厂短视频为什么总断更？怎么稳定持续产出",
  "desc": "很多厂起号猛、两周就断。断更比慢更伤。讲清断更的三个真原因和对应的可持续打法，稳比猛重要。",
  "category": "内容运营 · 操作类",
  "cat_label": "持续产出",
  "about": "工厂短视频持续产出",
  "card_meta": "操作 · 持续产出",
  "card_desc": "断更三因与可持续打法，稳比猛重要。",
  "lead": "很多厂起号猛、两周就断。断更比慢更伤。讲清断更的三个真原因和对应的可持续打法，稳比猛重要。",
  "sections": [
    ("h2", "原因一：把「拍视频」当额外任务"),
    ("p", "最易断根。把内容嵌进日常：巡检、打样、接待顺手拍，不单独抽时间，就不会「没空」，自然不断。"),
    ("h2", "原因二：每条都想「爆」"),
    ("p", "追求爆款压力太大。改成「每条解决一个小问题」，门槛低、可持续，爆款是副产品不是目标。"),
    ("h2", "原因三：没人牵头、没节奏"),
    ("p", "定一个负责人 + 固定发布节奏（如每周 3 条），像交付一样排期，断更概率大降。"),
    ("h2", "可持续的最小闭环"),
    ("p", "一个负责人、一套模板、一个固定频率、一个素材夹持续积累。小但稳，比断断续续强十倍。"),
    ("callout", "<strong>断更三因：当额外任务、求爆款、没人牵头。</strong>解法：嵌日常、做小不追爆、定人定频。稳比猛重要。"),
  ],
  "faq": [
    {"q": "一周发几条合适？", "a": "新手每周 2-3 条更稳，先保证不断，再求质和量。"},
    {"q": "没素材怎么办？", "a": "工厂天天有素材：车间、样品、客户问题都是。建个素材夹，随手存，永远不缺。"},
  ],
  "related": [
    {"href": "cong-0-dao-1.html", "title": "工厂抖音账号从 0 到 1 怎么起？"},
    {"href": "wei-shen-me-nan-zuo.html", "title": "制造业短视频，为什么多数工厂做不起来？"},
    {"href": "gong-chang-duan-shi-pin-jie-gou.html", "title": "工厂短视频脚本怎么写结构？B 端 5 段式模板"},
  ],
},
{
  "slug": "ping-tai-hong-xian",
  "title": "工厂做抖音要注意的平台红线，别踩违规",
  "desc": "违规一次限流、多次封号，号废了前面白干。工厂做抖音最常踩的几条红线，提前避开，号才活得久。",
  "category": "平台合规 · 红线",
  "cat_label": "平台红线",
  "about": "抖音平台合规红线",
  "card_meta": "合规 · 平台红线",
  "card_desc": "不实宣传、硬引流、搬运、缺资质，四条别踩。",
  "lead": "违规一次限流、多次封号，号废了前面白干。工厂做抖音最常踩的几条红线，提前避开，号才活得久。",
  "sections": [
    ("h2", "红线一：虚假宣传、夸大功效"),
    ("p", "别说「全网最低」「第一」「绝对」。工厂讲参数、讲案例要用真实数据，夸张表述既违规又伤信任，长期得不偿失。"),
    ("h2", "红线二：引导站外、私信骚扰"),
    ("p", "平台对「诱导加微信」有尺度。可以自然引导，但别在视频里硬塞联系方式、别私信狂轰。用主页和合规组件承接更稳。"),
    ("h2", "红线三：搬运、抄袭、侵权"),
    ("p", "别直接用别人视频、音乐、商标。原创或获授权，工厂实拍最安全也最加分，既合规又有辨识度。"),
    ("h2", "红线四：资质与行业特殊要求"),
    ("p", "某些品类（如医疗、金融、危化）有额外资质要求。发之前确认自己行业有没有特殊规则，别碰禁发内容。"),
    ("callout", "<strong>四条红线：不实宣传、硬引流、搬运侵权、缺资质。</strong>守住它们，号才活得久，内容才有积累。"),
  ],
  "faq": [
    {"q": "说「行业领先」算违规吗？", "a": "「领先」这类绝对化表述有风险，建议用可验证的说法（如「服务 X 家制造业客户」），避免无依据夸大。"},
    {"q": "被限流了怎么办？", "a": "先停违规内容，按平台规则整改，后续发合规原创养回权重，急不得。"},
  ],
  "related": [
    {"href": "shi-pin.html", "title": "工厂短视频怎么拍才不像自嗨？"},
    {"href": "dai-yun-ying-bi-keng.html", "title": "找工厂代运营怎么避坑？5 条硬标准筛掉不靠谱的"},
    {"href": "si-xin-hua-shu.html", "title": "抖音私信话术怎么写？客户主动问时这样接"},
  ],
},
]

def update_sitemap():
    with open(SITEMAP, encoding="utf-8") as f:
        content = f.read()
    new_urls = "\n".join(f"  <url><loc>{SITE}/articles/{a['slug']}</loc></url>" for a in ARTICLES)
    # 插在 </urlset> 之前
    marker = "</urlset>"
    assert marker in content, "sitemap 格式异常"
    content = content.replace(marker, new_urls + "\n" + marker, 1)
    with open(SITEMAP, "w", encoding="utf-8") as f:
        f.write(content)
    print("sitemap updated, +%d urls" % len(ARTICLES))

def update_index():
    with open(INDEX, encoding="utf-8") as f:
        content = f.read()
    # 构造新网格
    cards = []
    for a in ARTICLES:
        cards.append(
            f'        <a class="news-card" href="{a["slug"]}.html">\n'
            f'          <div class="news-card__meta">{a["card_meta"]}</div>\n'
            f'          <h3>{a["title"]}</h3>\n'
            f'          <p>{a["card_desc"]}</p>\n'
            f'          <span class="news-card__more">阅读 →</span>\n'
            f'        </a>'
        )
    grid = '      <div class="news-grid">\n' + "\n".join(cards) + '\n      </div>\n\n'
    marker = '      <div class="case-note"'
    assert marker in content, "index 结构异常"
    content = content.replace(marker, grid + '      <div class="case-note"', 1)
    # 更新计数
    content = content.replace("（41 篇）", "（51 篇）")
    content = content.replace("共41篇", "共51篇")
    content = content.replace("共36篇", "共51篇")
    with open(INDEX, "w", encoding="utf-8") as f:
        f.write(content)
    print("index updated, +%d cards" % len(ARTICLES))

if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    for a in ARTICLES:
        doc = render_article(a)
        path = os.path.join(OUT, a["slug"] + ".html")
        with open(path, "w", encoding="utf-8") as f:
            f.write(doc)
        print("written:", path, len(doc), "bytes")
    update_sitemap()
    update_index()
    print("TOTAL NEW:", len(ARTICLES))
