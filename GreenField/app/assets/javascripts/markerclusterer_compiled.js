


<!DOCTYPE html>
<html lang="en" class="">
  <head prefix="og: http://ogp.me/ns# fb: http://ogp.me/ns/fb# object: http://ogp.me/ns/object# article: http://ogp.me/ns/article# profile: http://ogp.me/ns/profile#">
    <meta charset='utf-8'>
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta http-equiv="Content-Language" content="en">
    <meta name="viewport" content="width=1020">
    
    
    <title>js-marker-clusterer/markerclusterer_compiled.js at gh-pages · googlemaps/js-marker-clusterer · GitHub</title>
    <link rel="search" type="application/opensearchdescription+xml" href="/opensearch.xml" title="GitHub">
    <link rel="fluid-icon" href="https://github.com/fluidicon.png" title="GitHub">
    <link rel="apple-touch-icon" sizes="57x57" href="/apple-touch-icon-114.png">
    <link rel="apple-touch-icon" sizes="114x114" href="/apple-touch-icon-114.png">
    <link rel="apple-touch-icon" sizes="72x72" href="/apple-touch-icon-144.png">
    <link rel="apple-touch-icon" sizes="144x144" href="/apple-touch-icon-144.png">
    <meta property="fb:app_id" content="1401488693436528">

      <meta content="@github" name="twitter:site" /><meta content="summary" name="twitter:card" /><meta content="googlemaps/js-marker-clusterer" name="twitter:title" /><meta content="js-marker-clusterer - A marker clustering library for the Google Maps JavaScript API v3." name="twitter:description" /><meta content="https://avatars0.githubusercontent.com/u/3717923?v=3&amp;s=400" name="twitter:image:src" />
      <meta content="GitHub" property="og:site_name" /><meta content="object" property="og:type" /><meta content="https://avatars0.githubusercontent.com/u/3717923?v=3&amp;s=400" property="og:image" /><meta content="googlemaps/js-marker-clusterer" property="og:title" /><meta content="https://github.com/googlemaps/js-marker-clusterer" property="og:url" /><meta content="js-marker-clusterer - A marker clustering library for the Google Maps JavaScript API v3." property="og:description" />
      <meta name="browser-stats-url" content="https://api.github.com/_private/browser/stats">
    <meta name="browser-errors-url" content="https://api.github.com/_private/browser/errors">
    <link rel="assets" href="https://assets-cdn.github.com/">
    
    <meta name="pjax-timeout" content="1000">
    

    <meta name="msapplication-TileImage" content="/windows-tile.png">
    <meta name="msapplication-TileColor" content="#ffffff">
    <meta name="selected-link" value="repo_source" data-pjax-transient>

        <meta name="google-analytics" content="UA-3769691-2">

    <meta content="collector.githubapp.com" name="octolytics-host" /><meta content="collector-cdn.github.com" name="octolytics-script-host" /><meta content="github" name="octolytics-app-id" /><meta content="80EDB632:3105:954DA2E:559D8D25" name="octolytics-dimension-request_id" />
    
    <meta content="Rails, view, blob#show" name="analytics-event" />
    <meta class="js-ga-set" name="dimension1" content="Logged Out">
    <meta name="is-dotcom" content="true">
      <meta name="hostname" content="github.com">
    <meta name="user-login" content="">

      <link rel="icon" sizes="any" mask href="https://assets-cdn.github.com/pinned-octocat.svg">
      <meta name="theme-color" content="#4078c0">
      <link rel="icon" type="image/x-icon" href="https://assets-cdn.github.com/favicon.ico">


    <meta content="authenticity_token" name="csrf-param" />
<meta content="UtGd1GDyyT8O4N2bOh4adjqqlmgYUM7V1+btTZnWyQxqUIBhiV98g6iwbSMkervmP7o2p7ntIMynn0TDW7IKtQ==" name="csrf-token" />

    <link crossorigin="anonymous" href="https://assets-cdn.github.com/assets/github/index-507b4f74c65565efec0273ea4338465df92b14c967ae71c2bda03dd97946b558.css" media="all" rel="stylesheet" />
    <link crossorigin="anonymous" href="https://assets-cdn.github.com/assets/github2/index-cc783bc128bbfd5d8ff80ccbb214b11c0ea7c0317a4643167906abe3ec25dac6.css" media="all" rel="stylesheet" />
    
    


    <meta http-equiv="x-pjax-version" content="26bd0557653f0b4777c28a2d4cfc74a5">

      
  <meta name="description" content="js-marker-clusterer - A marker clustering library for the Google Maps JavaScript API v3.">
  <meta name="go-import" content="github.com/googlemaps/js-marker-clusterer git https://github.com/googlemaps/js-marker-clusterer.git">

  <meta content="3717923" name="octolytics-dimension-user_id" /><meta content="googlemaps" name="octolytics-dimension-user_login" /><meta content="23974072" name="octolytics-dimension-repository_id" /><meta content="googlemaps/js-marker-clusterer" name="octolytics-dimension-repository_nwo" /><meta content="true" name="octolytics-dimension-repository_public" /><meta content="false" name="octolytics-dimension-repository_is_fork" /><meta content="23974072" name="octolytics-dimension-repository_network_root_id" /><meta content="googlemaps/js-marker-clusterer" name="octolytics-dimension-repository_network_root_nwo" />
  <link href="https://github.com/googlemaps/js-marker-clusterer/commits/gh-pages.atom" rel="alternate" title="Recent Commits to js-marker-clusterer:gh-pages" type="application/atom+xml">

  </head>


  <body class="logged_out  env-production linux vis-public page-blob">
    <a href="#start-of-content" tabindex="1" class="accessibility-aid js-skip-to-content">Skip to content</a>
    <div class="wrapper">
      
      
      



        
        <div class="header header-logged-out" role="banner">
  <div class="container clearfix">

    <a class="header-logo-wordmark" href="https://github.com/" data-ga-click="(Logged out) Header, go to homepage, icon:logo-wordmark">
      <span class="mega-octicon octicon-logo-github"></span>
    </a>

    <div class="header-actions" role="navigation">
        <a class="btn btn-primary" href="/join" data-ga-click="(Logged out) Header, clicked Sign up, text:sign-up">Sign up</a>
      <a class="btn" href="/login?return_to=%2Fgooglemaps%2Fjs-marker-clusterer%2Fblob%2Fgh-pages%2Fsrc%2Fmarkerclusterer_compiled.js" data-ga-click="(Logged out) Header, clicked Sign in, text:sign-in">Sign in</a>
    </div>

    <div class="site-search repo-scope js-site-search" role="search">
      <form accept-charset="UTF-8" action="/googlemaps/js-marker-clusterer/search" class="js-site-search-form" data-global-search-url="/search" data-repo-search-url="/googlemaps/js-marker-clusterer/search" method="get"><div style="margin:0;padding:0;display:inline"><input name="utf8" type="hidden" value="&#x2713;" /></div>
  <label class="js-chromeless-input-container form-control">
    <div class="scope-badge">This repository</div>
    <input type="text"
      class="js-site-search-focus js-site-search-field is-clearable chromeless-input"
      data-hotkey="s"
      name="q"
      placeholder="Search"
      data-global-scope-placeholder="Search GitHub"
      data-repo-scope-placeholder="Search"
      tabindex="1"
      autocapitalize="off">
  </label>
</form>
    </div>

      <ul class="header-nav left" role="navigation">
          <li class="header-nav-item">
            <a class="header-nav-link" href="/explore" data-ga-click="(Logged out) Header, go to explore, text:explore">Explore</a>
          </li>
          <li class="header-nav-item">
            <a class="header-nav-link" href="/features" data-ga-click="(Logged out) Header, go to features, text:features">Features</a>
          </li>
          <li class="header-nav-item">
            <a class="header-nav-link" href="https://enterprise.github.com/" data-ga-click="(Logged out) Header, go to enterprise, text:enterprise">Enterprise</a>
          </li>
          <li class="header-nav-item">
            <a class="header-nav-link" href="/blog" data-ga-click="(Logged out) Header, go to blog, text:blog">Blog</a>
          </li>
      </ul>

  </div>
</div>



      <div id="start-of-content" class="accessibility-aid"></div>
          <div class="site" itemscope itemtype="http://schema.org/WebPage">
    <div id="js-flash-container">
      
    </div>
    <div class="pagehead repohead instapaper_ignore readability-menu">
      <div class="container">

        
<ul class="pagehead-actions">

  <li>
      <a href="/login?return_to=%2Fgooglemaps%2Fjs-marker-clusterer"
    class="btn btn-sm btn-with-count tooltipped tooltipped-n"
    aria-label="You must be signed in to watch a repository" rel="nofollow">
    <span class="octicon octicon-eye"></span>
    Watch
  </a>
  <a class="social-count" href="/googlemaps/js-marker-clusterer/watchers">
    23
  </a>

  </li>

  <li>
      <a href="/login?return_to=%2Fgooglemaps%2Fjs-marker-clusterer"
    class="btn btn-sm btn-with-count tooltipped tooltipped-n"
    aria-label="You must be signed in to star a repository" rel="nofollow">
    <span class="octicon octicon-star"></span>
    Star
  </a>

    <a class="social-count js-social-count" href="/googlemaps/js-marker-clusterer/stargazers">
      209
    </a>

  </li>

    <li>
      <a href="/login?return_to=%2Fgooglemaps%2Fjs-marker-clusterer"
        class="btn btn-sm btn-with-count tooltipped tooltipped-n"
        aria-label="You must be signed in to fork a repository" rel="nofollow">
        <span class="octicon octicon-repo-forked"></span>
        Fork
      </a>
      <a href="/googlemaps/js-marker-clusterer/network" class="social-count">
        69
      </a>
    </li>
</ul>

        <h1 itemscope itemtype="http://data-vocabulary.org/Breadcrumb" class="entry-title public">
          <span class="mega-octicon octicon-repo"></span>
          <span class="author"><a href="/googlemaps" class="url fn" itemprop="url" rel="author"><span itemprop="title">googlemaps</span></a></span><!--
       --><span class="path-divider">/</span><!--
       --><strong><a href="/googlemaps/js-marker-clusterer" data-pjax="#js-repo-pjax-container">js-marker-clusterer</a></strong>

          <span class="page-context-loader">
            <img alt="" height="16" src="https://assets-cdn.github.com/images/spinners/octocat-spinner-32.gif" width="16" />
          </span>

        </h1>
      </div><!-- /.container -->
    </div><!-- /.repohead -->

    <div class="container">
      <div class="repository-with-sidebar repo-container new-discussion-timeline  ">
        <div class="repository-sidebar clearfix">
            
<nav class="sunken-menu repo-nav js-repo-nav js-sidenav-container-pjax js-octicon-loaders"
     role="navigation"
     data-pjax="#js-repo-pjax-container"
     data-issue-count-url="/googlemaps/js-marker-clusterer/issues/counts">
  <ul class="sunken-menu-group">
    <li class="tooltipped tooltipped-w" aria-label="Code">
      <a href="/googlemaps/js-marker-clusterer" aria-label="Code" class="selected js-selected-navigation-item sunken-menu-item" data-hotkey="g c" data-selected-links="repo_source repo_downloads repo_commits repo_releases repo_tags repo_branches /googlemaps/js-marker-clusterer">
        <span class="octicon octicon-code"></span> <span class="full-word">Code</span>
        <img alt="" class="mini-loader" height="16" src="https://assets-cdn.github.com/images/spinners/octocat-spinner-32.gif" width="16" />
</a>    </li>

      <li class="tooltipped tooltipped-w" aria-label="Issues">
        <a href="/googlemaps/js-marker-clusterer/issues" aria-label="Issues" class="js-selected-navigation-item sunken-menu-item" data-hotkey="g i" data-selected-links="repo_issues repo_labels repo_milestones /googlemaps/js-marker-clusterer/issues">
          <span class="octicon octicon-issue-opened"></span> <span class="full-word">Issues</span>
          <span class="js-issue-replace-counter"></span>
          <img alt="" class="mini-loader" height="16" src="https://assets-cdn.github.com/images/spinners/octocat-spinner-32.gif" width="16" />
</a>      </li>

    <li class="tooltipped tooltipped-w" aria-label="Pull requests">
      <a href="/googlemaps/js-marker-clusterer/pulls" aria-label="Pull requests" class="js-selected-navigation-item sunken-menu-item" data-hotkey="g p" data-selected-links="repo_pulls /googlemaps/js-marker-clusterer/pulls">
          <span class="octicon octicon-git-pull-request"></span> <span class="full-word">Pull requests</span>
          <span class="js-pull-replace-counter"></span>
          <img alt="" class="mini-loader" height="16" src="https://assets-cdn.github.com/images/spinners/octocat-spinner-32.gif" width="16" />
</a>    </li>

  </ul>
  <div class="sunken-menu-separator"></div>
  <ul class="sunken-menu-group">

    <li class="tooltipped tooltipped-w" aria-label="Pulse">
      <a href="/googlemaps/js-marker-clusterer/pulse" aria-label="Pulse" class="js-selected-navigation-item sunken-menu-item" data-selected-links="pulse /googlemaps/js-marker-clusterer/pulse">
        <span class="octicon octicon-pulse"></span> <span class="full-word">Pulse</span>
        <img alt="" class="mini-loader" height="16" src="https://assets-cdn.github.com/images/spinners/octocat-spinner-32.gif" width="16" />
</a>    </li>

    <li class="tooltipped tooltipped-w" aria-label="Graphs">
      <a href="/googlemaps/js-marker-clusterer/graphs" aria-label="Graphs" class="js-selected-navigation-item sunken-menu-item" data-selected-links="repo_graphs repo_contributors /googlemaps/js-marker-clusterer/graphs">
        <span class="octicon octicon-graph"></span> <span class="full-word">Graphs</span>
        <img alt="" class="mini-loader" height="16" src="https://assets-cdn.github.com/images/spinners/octocat-spinner-32.gif" width="16" />
</a>    </li>
  </ul>


</nav>

              <div class="only-with-full-nav">
                  
<div class="js-clone-url clone-url open"
  data-protocol-type="http">
  <h3><span class="text-emphasized">HTTPS</span> clone URL</h3>
  <div class="input-group js-zeroclipboard-container">
    <input type="text" class="input-mini input-monospace js-url-field js-zeroclipboard-target"
           value="https://github.com/googlemaps/js-marker-clusterer.git" readonly="readonly">
    <span class="input-group-button">
      <button aria-label="Copy to clipboard" class="js-zeroclipboard btn btn-sm zeroclipboard-button tooltipped tooltipped-s" data-copied-hint="Copied!" type="button"><span class="octicon octicon-clippy"></span></button>
    </span>
  </div>
</div>

  
<div class="js-clone-url clone-url "
  data-protocol-type="subversion">
  <h3><span class="text-emphasized">Subversion</span> checkout URL</h3>
  <div class="input-group js-zeroclipboard-container">
    <input type="text" class="input-mini input-monospace js-url-field js-zeroclipboard-target"
           value="https://github.com/googlemaps/js-marker-clusterer" readonly="readonly">
    <span class="input-group-button">
      <button aria-label="Copy to clipboard" class="js-zeroclipboard btn btn-sm zeroclipboard-button tooltipped tooltipped-s" data-copied-hint="Copied!" type="button"><span class="octicon octicon-clippy"></span></button>
    </span>
  </div>
</div>



<div class="clone-options">You can clone with
  <form accept-charset="UTF-8" action="/users/set_protocol?protocol_selector=http&amp;protocol_type=clone" class="inline-form js-clone-selector-form " data-remote="true" method="post"><div style="margin:0;padding:0;display:inline"><input name="utf8" type="hidden" value="&#x2713;" /><input name="authenticity_token" type="hidden" value="iNWwLwcgFRWgM9rB+Ytj1R6/OUB6kW/KBoo8y13TBgysWFubo13A7/qUtw9YuGNMmcxLmZh7uoelqioFk+AC0w==" /></div><button class="btn-link js-clone-selector" data-protocol="http" type="submit">HTTPS</button></form> or <form accept-charset="UTF-8" action="/users/set_protocol?protocol_selector=subversion&amp;protocol_type=clone" class="inline-form js-clone-selector-form " data-remote="true" method="post"><div style="margin:0;padding:0;display:inline"><input name="utf8" type="hidden" value="&#x2713;" /><input name="authenticity_token" type="hidden" value="MCui90GK58v5uSXlDrhTUh/aUf4jy5VWq0Qr3HG8/DwY5uI4H6SZajOh0yTMxmu90evuijjc1fvot/zj5gHjnw==" /></div><button class="btn-link js-clone-selector" data-protocol="subversion" type="submit">Subversion</button></form>.
  <a href="https://help.github.com/articles/which-remote-url-should-i-use" class="help tooltipped tooltipped-n" aria-label="Get help on which URL is right for you.">
    <span class="octicon octicon-question"></span>
  </a>
</div>




                <a href="/googlemaps/js-marker-clusterer/archive/gh-pages.zip"
                   class="btn btn-sm sidebar-button"
                   aria-label="Download the contents of googlemaps/js-marker-clusterer as a zip file"
                   title="Download the contents of googlemaps/js-marker-clusterer as a zip file"
                   rel="nofollow">
                  <span class="octicon octicon-cloud-download"></span>
                  Download ZIP
                </a>
              </div>
        </div><!-- /.repository-sidebar -->

        <div id="js-repo-pjax-container" class="repository-content context-loader-container" data-pjax-container>

          

<a href="/googlemaps/js-marker-clusterer/blob/89b08d0db5553f16a67653b049b3aebce9a7406a/src/markerclusterer_compiled.js" class="hidden js-permalink-shortcut" data-hotkey="y">Permalink</a>

<!-- blob contrib key: blob_contributors:v21:1bd90437ccb3414a21f922eb6acfa72d -->

<div class="file-navigation js-zeroclipboard-container">
  
<div class="select-menu js-menu-container js-select-menu left">
  <span class="btn btn-sm select-menu-button js-menu-target css-truncate" data-hotkey="w"
    data-ref="gh-pages"
    title="gh-pages"
    role="button" aria-label="Switch branches or tags" tabindex="0" aria-haspopup="true">
    <span class="octicon octicon-git-branch"></span>
    <i>branch:</i>
    <span class="js-select-button css-truncate-target">gh-pages</span>
  </span>

  <div class="select-menu-modal-holder js-menu-content js-navigation-container" data-pjax aria-hidden="true">

    <div class="select-menu-modal">
      <div class="select-menu-header">
        <span class="select-menu-title">Switch branches/tags</span>
        <span class="octicon octicon-x js-menu-close" role="button" aria-label="Close"></span>
      </div>

      <div class="select-menu-filters">
        <div class="select-menu-text-filter">
          <input type="text" aria-label="Filter branches/tags" id="context-commitish-filter-field" class="js-filterable-field js-navigation-enable" placeholder="Filter branches/tags">
        </div>
        <div class="select-menu-tabs">
          <ul>
            <li class="select-menu-tab">
              <a href="#" data-tab-filter="branches" data-filter-placeholder="Filter branches/tags" class="js-select-menu-tab">Branches</a>
            </li>
            <li class="select-menu-tab">
              <a href="#" data-tab-filter="tags" data-filter-placeholder="Find a tag…" class="js-select-menu-tab">Tags</a>
            </li>
          </ul>
        </div>
      </div>

      <div class="select-menu-list select-menu-tab-bucket js-select-menu-tab-bucket" data-tab-filter="branches">

        <div data-filterable-for="context-commitish-filter-field" data-filterable-type="substring">


            <a class="select-menu-item js-navigation-item js-navigation-open selected"
               href="/googlemaps/js-marker-clusterer/blob/gh-pages/src/markerclusterer_compiled.js"
               data-name="gh-pages"
               data-skip-pjax="true"
               rel="nofollow">
              <span class="select-menu-item-icon octicon octicon-check"></span>
              <span class="select-menu-item-text css-truncate-target" title="gh-pages">
                gh-pages
              </span>
            </a>
        </div>

          <div class="select-menu-no-results">Nothing to show</div>
      </div>

      <div class="select-menu-list select-menu-tab-bucket js-select-menu-tab-bucket" data-tab-filter="tags">
        <div data-filterable-for="context-commitish-filter-field" data-filterable-type="substring">


        </div>

        <div class="select-menu-no-results">Nothing to show</div>
      </div>

    </div>
  </div>
</div>

  <div class="btn-group right">
    <a href="/googlemaps/js-marker-clusterer/find/gh-pages"
          class="js-show-file-finder btn btn-sm empty-icon tooltipped tooltipped-s"
          data-pjax
          data-hotkey="t"
          aria-label="Quickly jump between files">
      <span class="octicon octicon-list-unordered"></span>
    </a>
    <button aria-label="Copy file path to clipboard" class="js-zeroclipboard btn btn-sm zeroclipboard-button tooltipped tooltipped-s" data-copied-hint="Copied!" type="button"><span class="octicon octicon-clippy"></span></button>
  </div>

  <div class="breadcrumb js-zeroclipboard-target">
    <span class="repo-root js-repo-root"><span itemscope="" itemtype="http://data-vocabulary.org/Breadcrumb"><a href="/googlemaps/js-marker-clusterer" class="" data-branch="gh-pages" data-pjax="true" itemscope="url"><span itemprop="title">js-marker-clusterer</span></a></span></span><span class="separator">/</span><span itemscope="" itemtype="http://data-vocabulary.org/Breadcrumb"><a href="/googlemaps/js-marker-clusterer/tree/gh-pages/src" class="" data-branch="gh-pages" data-pjax="true" itemscope="url"><span itemprop="title">src</span></a></span><span class="separator">/</span><strong class="final-path">markerclusterer_compiled.js</strong>
  </div>
</div>


  <div class="commit file-history-tease">
    <div class="file-history-tease-header">
        <img alt="@brendankenny" class="avatar" data-user="316891" height="24" src="https://avatars1.githubusercontent.com/u/316891?v=3&amp;s=48" width="24" />
        <span class="author"><a href="/brendankenny" rel="contributor">brendankenny</a></span>
        <time datetime="2014-09-12T19:46:15Z" is="relative-time">Sep 12, 2014</time>
        <div class="commit-title">
            <a href="/googlemaps/js-marker-clusterer/commit/47539103e8cec3c8e3944e939f08e667904805db" class="message" data-pjax="true" title="transfer to github">transfer to github</a>
        </div>
    </div>

    <div class="participation">
      <p class="quickstat">
        <a href="#blob_contributors_box" rel="facebox">
          <strong>1</strong>
           contributor
        </a>
      </p>
      
    </div>
    <div id="blob_contributors_box" style="display:none">
      <h2 class="facebox-header">Users who have contributed to this file</h2>
      <ul class="facebox-user-list">
          <li class="facebox-user-list-item">
            <img alt="@brendankenny" data-user="316891" height="24" src="https://avatars1.githubusercontent.com/u/316891?v=3&amp;s=48" width="24" />
            <a href="/brendankenny">brendankenny</a>
          </li>
      </ul>
    </div>
  </div>

<div class="file">
  <div class="file-header">
    <div class="file-actions">

      <div class="btn-group">
        <a href="/googlemaps/js-marker-clusterer/raw/gh-pages/src/markerclusterer_compiled.js" class="btn btn-sm " id="raw-url">Raw</a>
          <a href="/googlemaps/js-marker-clusterer/blame/gh-pages/src/markerclusterer_compiled.js" class="btn btn-sm js-update-url-with-hash">Blame</a>
        <a href="/googlemaps/js-marker-clusterer/commits/gh-pages/src/markerclusterer_compiled.js" class="btn btn-sm " rel="nofollow">History</a>
      </div>


          <button type="button" class="octicon-btn disabled tooltipped tooltipped-n" aria-label="You must be signed in to make or propose changes">
            <span class="octicon octicon-pencil"></span>
          </button>

        <button type="button" class="octicon-btn octicon-btn-danger disabled tooltipped tooltipped-n" aria-label="You must be signed in to make or propose changes">
          <span class="octicon octicon-trashcan"></span>
        </button>
    </div>

    <div class="file-info">
        21 lines (21 sloc)
        <span class="file-info-divider"></span>
      7.984 kB
    </div>
  </div>
  

  <div class="blob-wrapper data type-javascript">
      <table class="highlight tab-size js-file-line-container" data-tab-size="8">
      <tr>
        <td id="L1" class="blob-num js-line-number" data-line-number="1"></td>
        <td id="LC1" class="blob-code blob-code-inner js-file-line">(<span class="pl-k">function</span>(){<span class="pl-k">var</span> d<span class="pl-k">=</span><span class="pl-c1">null</span>;<span class="pl-k">function</span> <span class="pl-en">e</span>(<span class="pl-smi">a</span>){<span class="pl-k">return</span> <span class="pl-k">function</span>(<span class="pl-smi">b</span>){<span class="pl-v">this</span>[a]<span class="pl-k">=</span>b}}<span class="pl-k">function</span> <span class="pl-en">h</span>(<span class="pl-smi">a</span>){<span class="pl-k">return</span> <span class="pl-k">function</span>(){<span class="pl-k">return</span> <span class="pl-v">this</span>[a]}}<span class="pl-k">var</span> j;</td>
      </tr>
      <tr>
        <td id="L2" class="blob-num js-line-number" data-line-number="2"></td>
        <td id="LC2" class="blob-code blob-code-inner js-file-line"><span class="pl-k">function</span> <span class="pl-en">k</span>(<span class="pl-smi">a</span>,<span class="pl-smi">b</span>,<span class="pl-smi">c</span>){<span class="pl-v">this</span>.extend(k,google.maps.OverlayView);<span class="pl-v">this</span>.c<span class="pl-k">=</span>a;<span class="pl-v">this</span>.a<span class="pl-k">=</span>[];<span class="pl-v">this</span>.f<span class="pl-k">=</span>[];<span class="pl-v">this</span>.ca<span class="pl-k">=</span>[<span class="pl-c1">53</span>,<span class="pl-c1">56</span>,<span class="pl-c1">66</span>,<span class="pl-c1">78</span>,<span class="pl-c1">90</span>];<span class="pl-v">this</span>.j<span class="pl-k">=</span>[];<span class="pl-v">this</span>.A<span class="pl-k">=!</span><span class="pl-c1">1</span>;c<span class="pl-k">=</span>c<span class="pl-k">||</span>{};<span class="pl-v">this</span>.g<span class="pl-k">=</span>c.gridSize<span class="pl-k">||</span><span class="pl-c1">60</span>;<span class="pl-v">this</span>.l<span class="pl-k">=</span>c.minimumClusterSize<span class="pl-k">||</span><span class="pl-c1">2</span>;<span class="pl-v">this</span>.J<span class="pl-k">=</span>c.maxZoom<span class="pl-k">||</span>d;<span class="pl-v">this</span>.j<span class="pl-k">=</span>c.styles<span class="pl-k">||</span>[];<span class="pl-v">this</span>.X<span class="pl-k">=</span>c.imagePath<span class="pl-k">||</span><span class="pl-v">this</span>.Q;<span class="pl-v">this</span>.W<span class="pl-k">=</span>c.imageExtension<span class="pl-k">||</span><span class="pl-v">this</span>.P;<span class="pl-v">this</span>.O<span class="pl-k">=!</span><span class="pl-c1">0</span>;<span class="pl-k">if</span>(c.zoomOnClick<span class="pl-k">!=void</span> <span class="pl-c1">0</span>)<span class="pl-v">this</span>.O<span class="pl-k">=</span>c.zoomOnClick;<span class="pl-v">this</span>.r<span class="pl-k">=!</span><span class="pl-c1">1</span>;<span class="pl-k">if</span>(c.averageCenter<span class="pl-k">!=void</span> <span class="pl-c1">0</span>)<span class="pl-v">this</span>.r<span class="pl-k">=</span>c.averageCenter;l(<span class="pl-v">this</span>);<span class="pl-v">this</span>.setMap(a);<span class="pl-v">this</span>.K<span class="pl-k">=</span><span class="pl-v">this</span>.c.getZoom();<span class="pl-k">var</span> f<span class="pl-k">=</span><span class="pl-v">this</span>;google.maps.<span class="pl-c1">event</span>.addListener(<span class="pl-v">this</span>.c,</td>
      </tr>
      <tr>
        <td id="L3" class="blob-num js-line-number" data-line-number="3"></td>
        <td id="LC3" class="blob-code blob-code-inner js-file-line"><span class="pl-s"><span class="pl-pds">&quot;</span>zoom_changed<span class="pl-pds">&quot;</span></span>,<span class="pl-k">function</span>(){<span class="pl-k">var</span> a<span class="pl-k">=</span>f.c.getZoom();<span class="pl-k">if</span>(f.K<span class="pl-k">!=</span>a)f.K<span class="pl-k">=</span>a,f.m()});google.maps.<span class="pl-c1">event</span>.addListener(<span class="pl-v">this</span>.c,<span class="pl-s"><span class="pl-pds">&quot;</span>idle<span class="pl-pds">&quot;</span></span>,<span class="pl-k">function</span>(){f.i()});b<span class="pl-k">&amp;&amp;</span>b.<span class="pl-c1">length</span><span class="pl-k">&amp;&amp;</span><span class="pl-v">this</span>.C(b,<span class="pl-k">!</span><span class="pl-c1">1</span>)}j<span class="pl-k">=</span>k.<span class="pl-c1">prototype</span>;j.Q<span class="pl-k">=</span><span class="pl-s"><span class="pl-pds">&quot;</span>http://google-maps-utility-library-v3.googlecode.com/svn/trunk/markerclusterer/images/m<span class="pl-pds">&quot;</span></span>;j.P<span class="pl-k">=</span><span class="pl-s"><span class="pl-pds">&quot;</span>png<span class="pl-pds">&quot;</span></span>;<span class="pl-c1">j</span>.<span class="pl-en">extend</span><span class="pl-k">=</span><span class="pl-k">function</span>(<span class="pl-smi">a</span>,<span class="pl-smi">b</span>){<span class="pl-k">return</span> <span class="pl-k">function</span>(<span class="pl-smi">a</span>){<span class="pl-k">for</span>(<span class="pl-k">var</span> b <span class="pl-k">in</span> a.<span class="pl-c1">prototype</span>)<span class="pl-v">this</span>.<span class="pl-c1">prototype</span>[b]<span class="pl-k">=</span>a.<span class="pl-c1">prototype</span>[b];<span class="pl-k">return</span> <span class="pl-v">this</span>}.<span class="pl-c1">apply</span>(a,[b])};<span class="pl-c1">j</span>.<span class="pl-en">onAdd</span><span class="pl-k">=</span><span class="pl-k">function</span>(){<span class="pl-k">if</span>(<span class="pl-k">!</span><span class="pl-v">this</span>.A)<span class="pl-v">this</span>.A<span class="pl-k">=!</span><span class="pl-c1">0</span>,n(<span class="pl-v">this</span>)};<span class="pl-c1">j</span>.<span class="pl-en">draw</span><span class="pl-k">=</span><span class="pl-k">function</span>(){};</td>
      </tr>
      <tr>
        <td id="L4" class="blob-num js-line-number" data-line-number="4"></td>
        <td id="LC4" class="blob-code blob-code-inner js-file-line"><span class="pl-k">function</span> <span class="pl-en">l</span>(<span class="pl-smi">a</span>){<span class="pl-k">if</span>(<span class="pl-k">!</span>a.j.<span class="pl-c1">length</span>)<span class="pl-k">for</span>(<span class="pl-k">var</span> b<span class="pl-k">=</span><span class="pl-c1">0</span>,c;c<span class="pl-k">=</span>a.ca[b];b<span class="pl-k">++</span>)a.j.<span class="pl-c1">push</span>({url<span class="pl-k">:</span>a.X<span class="pl-k">+</span>(b<span class="pl-k">+</span><span class="pl-c1">1</span>)<span class="pl-k">+</span><span class="pl-s"><span class="pl-pds">&quot;</span>.<span class="pl-pds">&quot;</span></span><span class="pl-k">+</span>a.W,height<span class="pl-k">:</span>c,width<span class="pl-k">:</span>c})}<span class="pl-c1">j</span>.<span class="pl-en">S</span><span class="pl-k">=</span><span class="pl-k">function</span>(){<span class="pl-k">for</span>(<span class="pl-k">var</span> a<span class="pl-k">=</span><span class="pl-v">this</span>.o(),b<span class="pl-k">=</span><span class="pl-k">new</span> <span class="pl-en">google.maps</span>.LatLngBounds,c<span class="pl-k">=</span><span class="pl-c1">0</span>,f;f<span class="pl-k">=</span>a[c];c<span class="pl-k">++</span>)b.extend(f.getPosition());<span class="pl-v">this</span>.c.fitBounds(b)};j.<span class="pl-c1">z</span><span class="pl-k">=</span>h(<span class="pl-s"><span class="pl-pds">&quot;</span>j<span class="pl-pds">&quot;</span></span>);j.o<span class="pl-k">=</span>h(<span class="pl-s"><span class="pl-pds">&quot;</span>a<span class="pl-pds">&quot;</span></span>);<span class="pl-c1">j</span>.<span class="pl-en">V</span><span class="pl-k">=</span><span class="pl-k">function</span>(){<span class="pl-k">return</span> <span class="pl-v">this</span>.a.<span class="pl-c1">length</span>};j.ba<span class="pl-k">=</span>e(<span class="pl-s"><span class="pl-pds">&quot;</span>J<span class="pl-pds">&quot;</span></span>);j.I<span class="pl-k">=</span>h(<span class="pl-s"><span class="pl-pds">&quot;</span>J<span class="pl-pds">&quot;</span></span>);<span class="pl-c1">j</span>.<span class="pl-en">G</span><span class="pl-k">=</span><span class="pl-k">function</span>(<span class="pl-smi">a</span>,<span class="pl-smi">b</span>){<span class="pl-k">for</span>(<span class="pl-k">var</span> c<span class="pl-k">=</span><span class="pl-c1">0</span>,f<span class="pl-k">=</span>a.<span class="pl-c1">length</span>,g<span class="pl-k">=</span>f;g<span class="pl-k">!==</span><span class="pl-c1">0</span>;)g<span class="pl-k">=</span><span class="pl-c1">parseInt</span>(g/<span class="pl-c1">10</span>,<span class="pl-c1">10</span>),c<span class="pl-k">++</span>;c<span class="pl-k">=</span><span class="pl-c1">Math</span>.<span class="pl-c1">min</span>(c,b);<span class="pl-k">return</span>{text<span class="pl-k">:</span>f,index<span class="pl-k">:</span>c}};j.$<span class="pl-k">=</span>e(<span class="pl-s"><span class="pl-pds">&quot;</span>G<span class="pl-pds">&quot;</span></span>);j.H<span class="pl-k">=</span>h(<span class="pl-s"><span class="pl-pds">&quot;</span>G<span class="pl-pds">&quot;</span></span>);</td>
      </tr>
      <tr>
        <td id="L5" class="blob-num js-line-number" data-line-number="5"></td>
        <td id="LC5" class="blob-code blob-code-inner js-file-line"><span class="pl-c1">j</span>.<span class="pl-en">C</span><span class="pl-k">=</span><span class="pl-k">function</span>(<span class="pl-smi">a</span>,<span class="pl-smi">b</span>){<span class="pl-k">for</span>(<span class="pl-k">var</span> c<span class="pl-k">=</span><span class="pl-c1">0</span>,f;f<span class="pl-k">=</span>a[c];c<span class="pl-k">++</span>)q(<span class="pl-v">this</span>,f);b<span class="pl-k">||</span><span class="pl-v">this</span>.i()};<span class="pl-k">function</span> <span class="pl-en">q</span>(<span class="pl-smi">a</span>,<span class="pl-smi">b</span>){b.s<span class="pl-k">=!</span><span class="pl-c1">1</span>;b.draggable<span class="pl-k">&amp;&amp;</span>google.maps.<span class="pl-c1">event</span>.addListener(b,<span class="pl-s"><span class="pl-pds">&quot;</span>dragend<span class="pl-pds">&quot;</span></span>,<span class="pl-k">function</span>(){b.s<span class="pl-k">=!</span><span class="pl-c1">1</span>;a.L()});a.a.<span class="pl-c1">push</span>(b)}<span class="pl-c1">j</span>.<span class="pl-en">q</span><span class="pl-k">=</span><span class="pl-k">function</span>(<span class="pl-smi">a</span>,<span class="pl-smi">b</span>){q(<span class="pl-v">this</span>,a);b<span class="pl-k">||</span><span class="pl-v">this</span>.i()};<span class="pl-k">function</span> <span class="pl-en">r</span>(<span class="pl-smi">a</span>,<span class="pl-smi">b</span>){<span class="pl-k">var</span> c<span class="pl-k">=-</span><span class="pl-c1">1</span>;<span class="pl-k">if</span>(a.a.indexOf)c<span class="pl-k">=</span>a.a.<span class="pl-c1">indexOf</span>(b);<span class="pl-k">else</span> <span class="pl-k">for</span>(<span class="pl-k">var</span> f<span class="pl-k">=</span><span class="pl-c1">0</span>,g;g<span class="pl-k">=</span>a.a[f];f<span class="pl-k">++</span>)<span class="pl-k">if</span>(g<span class="pl-k">==</span>b){c<span class="pl-k">=</span>f;<span class="pl-k">break</span>}<span class="pl-k">if</span>(c<span class="pl-k">==-</span><span class="pl-c1">1</span>)<span class="pl-k">return</span><span class="pl-k">!</span><span class="pl-c1">1</span>;b.setMap(d);a.a.<span class="pl-c1">splice</span>(c,<span class="pl-c1">1</span>);<span class="pl-k">return</span><span class="pl-k">!</span><span class="pl-c1">0</span>}<span class="pl-c1">j</span>.<span class="pl-en">Y</span><span class="pl-k">=</span><span class="pl-k">function</span>(<span class="pl-smi">a</span>,<span class="pl-smi">b</span>){<span class="pl-k">var</span> c<span class="pl-k">=</span>r(<span class="pl-v">this</span>,a);<span class="pl-k">return</span><span class="pl-k">!</span>b<span class="pl-k">&amp;&amp;</span>c<span class="pl-k">?</span>(<span class="pl-v">this</span>.m(),<span class="pl-v">this</span>.i(),<span class="pl-k">!</span><span class="pl-c1">0</span>)<span class="pl-k">:!</span><span class="pl-c1">1</span>};</td>
      </tr>
      <tr>
        <td id="L6" class="blob-num js-line-number" data-line-number="6"></td>
        <td id="LC6" class="blob-code blob-code-inner js-file-line"><span class="pl-c1">j</span>.<span class="pl-en">Z</span><span class="pl-k">=</span><span class="pl-k">function</span>(<span class="pl-smi">a</span>,<span class="pl-smi">b</span>){<span class="pl-k">for</span>(<span class="pl-k">var</span> c<span class="pl-k">=!</span><span class="pl-c1">1</span>,f<span class="pl-k">=</span><span class="pl-c1">0</span>,g;g<span class="pl-k">=</span>a[f];f<span class="pl-k">++</span>)g<span class="pl-k">=</span>r(<span class="pl-v">this</span>,g),c<span class="pl-k">=</span>c<span class="pl-k">||</span>g;<span class="pl-k">if</span>(<span class="pl-k">!</span>b<span class="pl-k">&amp;&amp;</span>c)<span class="pl-k">return</span> <span class="pl-v">this</span>.m(),<span class="pl-v">this</span>.i(),<span class="pl-k">!</span><span class="pl-c1">0</span>};<span class="pl-c1">j</span>.<span class="pl-en">U</span><span class="pl-k">=</span><span class="pl-k">function</span>(){<span class="pl-k">return</span> <span class="pl-v">this</span>.f.<span class="pl-c1">length</span>};j.getMap<span class="pl-k">=</span>h(<span class="pl-s"><span class="pl-pds">&quot;</span>c<span class="pl-pds">&quot;</span></span>);j.setMap<span class="pl-k">=</span>e(<span class="pl-s"><span class="pl-pds">&quot;</span>c<span class="pl-pds">&quot;</span></span>);j.w<span class="pl-k">=</span>h(<span class="pl-s"><span class="pl-pds">&quot;</span>g<span class="pl-pds">&quot;</span></span>);j.aa<span class="pl-k">=</span>e(<span class="pl-s"><span class="pl-pds">&quot;</span>g<span class="pl-pds">&quot;</span></span>);</td>
      </tr>
      <tr>
        <td id="L7" class="blob-num js-line-number" data-line-number="7"></td>
        <td id="LC7" class="blob-code blob-code-inner js-file-line"><span class="pl-c1">j</span>.<span class="pl-en">v</span><span class="pl-k">=</span><span class="pl-k">function</span>(<span class="pl-smi">a</span>){<span class="pl-k">var</span> b<span class="pl-k">=</span><span class="pl-v">this</span>.getProjection(),c<span class="pl-k">=</span><span class="pl-k">new</span> <span class="pl-en">google.maps</span>.LatLng(a.getNorthEast().lat(),a.getNorthEast().lng()),f<span class="pl-k">=</span><span class="pl-k">new</span> <span class="pl-en">google.maps</span>.LatLng(a.getSouthWest().lat(),a.getSouthWest().lng()),c<span class="pl-k">=</span>b.fromLatLngToDivPixel(c);c.<span class="pl-c1">x</span><span class="pl-k">+=</span><span class="pl-v">this</span>.g;c.<span class="pl-c1">y</span><span class="pl-k">-=</span><span class="pl-v">this</span>.g;f<span class="pl-k">=</span>b.fromLatLngToDivPixel(f);f.<span class="pl-c1">x</span><span class="pl-k">-=</span><span class="pl-v">this</span>.g;f.<span class="pl-c1">y</span><span class="pl-k">+=</span><span class="pl-v">this</span>.g;c<span class="pl-k">=</span>b.fromDivPixelToLatLng(c);b<span class="pl-k">=</span>b.fromDivPixelToLatLng(f);a.extend(c);a.extend(b);<span class="pl-k">return</span> a};<span class="pl-c1">j</span>.<span class="pl-en">R</span><span class="pl-k">=</span><span class="pl-k">function</span>(){<span class="pl-v">this</span>.m(<span class="pl-k">!</span><span class="pl-c1">0</span>);<span class="pl-v">this</span>.a<span class="pl-k">=</span>[]};</td>
      </tr>
      <tr>
        <td id="L8" class="blob-num js-line-number" data-line-number="8"></td>
        <td id="LC8" class="blob-code blob-code-inner js-file-line"><span class="pl-c1">j</span>.<span class="pl-en">m</span><span class="pl-k">=</span><span class="pl-k">function</span>(<span class="pl-smi">a</span>){<span class="pl-k">for</span>(<span class="pl-k">var</span> b<span class="pl-k">=</span><span class="pl-c1">0</span>,c;c<span class="pl-k">=</span><span class="pl-v">this</span>.f[b];b<span class="pl-k">++</span>)c.remove();<span class="pl-k">for</span>(b<span class="pl-k">=</span><span class="pl-c1">0</span>;c<span class="pl-k">=</span><span class="pl-v">this</span>.a[b];b<span class="pl-k">++</span>)c.s<span class="pl-k">=!</span><span class="pl-c1">1</span>,a<span class="pl-k">&amp;&amp;</span>c.setMap(d);<span class="pl-v">this</span>.f<span class="pl-k">=</span>[]};<span class="pl-c1">j</span>.<span class="pl-en">L</span><span class="pl-k">=</span><span class="pl-k">function</span>(){<span class="pl-k">var</span> a<span class="pl-k">=</span><span class="pl-v">this</span>.f.<span class="pl-c1">slice</span>();<span class="pl-v">this</span>.f.<span class="pl-c1">length</span><span class="pl-k">=</span><span class="pl-c1">0</span>;<span class="pl-v">this</span>.m();<span class="pl-v">this</span>.i();<span class="pl-c1">window</span>.<span class="pl-c1">setTimeout</span>(<span class="pl-k">function</span>(){<span class="pl-k">for</span>(<span class="pl-k">var</span> b<span class="pl-k">=</span><span class="pl-c1">0</span>,c;c<span class="pl-k">=</span>a[b];b<span class="pl-k">++</span>)c.remove()},<span class="pl-c1">0</span>)};<span class="pl-c1">j</span>.<span class="pl-en">i</span><span class="pl-k">=</span><span class="pl-k">function</span>(){n(<span class="pl-v">this</span>)};</td>
      </tr>
      <tr>
        <td id="L9" class="blob-num js-line-number" data-line-number="9"></td>
        <td id="LC9" class="blob-code blob-code-inner js-file-line"><span class="pl-k">function</span> <span class="pl-en">n</span>(<span class="pl-smi">a</span>){<span class="pl-k">if</span>(a.A)<span class="pl-k">for</span>(<span class="pl-k">var</span> b<span class="pl-k">=</span>a.v(<span class="pl-k">new</span> <span class="pl-en">google.maps</span>.LatLngBounds(a.c.getBounds().getSouthWest(),a.c.getBounds().getNorthEast())),c<span class="pl-k">=</span><span class="pl-c1">0</span>,f;f<span class="pl-k">=</span>a.a[c];c<span class="pl-k">++</span>)<span class="pl-k">if</span>(<span class="pl-k">!</span>f.s<span class="pl-k">&amp;&amp;</span>b.contains(f.getPosition())){<span class="pl-k">for</span>(<span class="pl-k">var</span> g<span class="pl-k">=</span>a,u<span class="pl-k">=</span><span class="pl-c1">4E4</span>,o<span class="pl-k">=</span>d,v<span class="pl-k">=</span><span class="pl-c1">0</span>,m<span class="pl-k">=void</span> <span class="pl-c1">0</span>;m<span class="pl-k">=</span>g.f[v];v<span class="pl-k">++</span>){<span class="pl-k">var</span> i<span class="pl-k">=</span>m.getCenter();<span class="pl-k">if</span>(i){<span class="pl-k">var</span> p<span class="pl-k">=</span>f.getPosition();<span class="pl-k">if</span>(<span class="pl-k">!</span>i<span class="pl-k">||!</span>p)i<span class="pl-k">=</span><span class="pl-c1">0</span>;<span class="pl-k">else</span> <span class="pl-k">var</span> w<span class="pl-k">=</span>(p.lat()<span class="pl-k">-</span>i.lat())<span class="pl-k">*</span><span class="pl-c1">Math</span>.<span class="pl-c1">PI</span>/<span class="pl-c1">180</span>,x<span class="pl-k">=</span>(p.lng()<span class="pl-k">-</span>i.lng())<span class="pl-k">*</span><span class="pl-c1">Math</span>.<span class="pl-c1">PI</span>/<span class="pl-c1">180</span>,i<span class="pl-k">=</span><span class="pl-c1">Math</span>.<span class="pl-c1">sin</span>(w/<span class="pl-c1">2</span>)<span class="pl-k">*</span><span class="pl-c1">Math</span>.<span class="pl-c1">sin</span>(w/<span class="pl-c1">2</span>)<span class="pl-k">+</span><span class="pl-c1">Math</span>.<span class="pl-c1">cos</span>(i.lat()<span class="pl-k">*</span><span class="pl-c1">Math</span>.<span class="pl-c1">PI</span>/<span class="pl-c1">180</span>)<span class="pl-k">*</span><span class="pl-c1">Math</span>.<span class="pl-c1">cos</span>(p.lat()<span class="pl-k">*</span><span class="pl-c1">Math</span>.<span class="pl-c1">PI</span>/<span class="pl-c1">180</span>)<span class="pl-k">*</span><span class="pl-c1">Math</span>.<span class="pl-c1">sin</span>(x/<span class="pl-c1">2</span>)<span class="pl-k">*</span><span class="pl-c1">Math</span>.<span class="pl-c1">sin</span>(x/<span class="pl-c1">2</span>),i<span class="pl-k">=</span><span class="pl-c1">6371</span><span class="pl-k">*</span><span class="pl-c1">2</span><span class="pl-k">*</span><span class="pl-c1">Math</span>.<span class="pl-c1">atan2</span>(<span class="pl-c1">Math</span>.<span class="pl-c1">sqrt</span>(i),</td>
      </tr>
      <tr>
        <td id="L10" class="blob-num js-line-number" data-line-number="10"></td>
        <td id="LC10" class="blob-code blob-code-inner js-file-line"><span class="pl-c1">Math</span>.<span class="pl-c1">sqrt</span>(<span class="pl-c1">1</span><span class="pl-k">-</span>i));i<span class="pl-k">&lt;</span>u<span class="pl-k">&amp;&amp;</span>(u<span class="pl-k">=</span>i,o<span class="pl-k">=</span>m)}}o<span class="pl-k">&amp;&amp;</span>o.F.contains(f.getPosition())<span class="pl-k">?</span>o.q(f)<span class="pl-k">:</span>(m<span class="pl-k">=</span><span class="pl-k">new</span> <span class="pl-en">s</span>(g),m.q(f),g.f.<span class="pl-c1">push</span>(m))}}<span class="pl-k">function</span> <span class="pl-en">s</span>(<span class="pl-smi">a</span>){<span class="pl-v">this</span>.k<span class="pl-k">=</span>a;<span class="pl-v">this</span>.c<span class="pl-k">=</span>a.getMap();<span class="pl-v">this</span>.g<span class="pl-k">=</span>a.w();<span class="pl-v">this</span>.l<span class="pl-k">=</span>a.l;<span class="pl-v">this</span>.r<span class="pl-k">=</span>a.r;<span class="pl-v">this</span>.d<span class="pl-k">=</span>d;<span class="pl-v">this</span>.a<span class="pl-k">=</span>[];<span class="pl-v">this</span>.F<span class="pl-k">=</span>d;<span class="pl-v">this</span>.n<span class="pl-k">=</span><span class="pl-k">new</span> <span class="pl-en">t</span>(<span class="pl-v">this</span>,a.<span class="pl-c1">z</span>(),a.w())}j<span class="pl-k">=</span>s.<span class="pl-c1">prototype</span>;</td>
      </tr>
      <tr>
        <td id="L11" class="blob-num js-line-number" data-line-number="11"></td>
        <td id="LC11" class="blob-code blob-code-inner js-file-line"><span class="pl-c1">j</span>.<span class="pl-en">q</span><span class="pl-k">=</span><span class="pl-k">function</span>(<span class="pl-smi">a</span>){<span class="pl-k">var</span> b;a<span class="pl-k">:</span><span class="pl-k">if</span>(<span class="pl-v">this</span>.a.indexOf)b<span class="pl-k">=</span><span class="pl-v">this</span>.a.<span class="pl-c1">indexOf</span>(a)<span class="pl-k">!=-</span><span class="pl-c1">1</span>;<span class="pl-k">else</span>{b<span class="pl-k">=</span><span class="pl-c1">0</span>;<span class="pl-k">for</span>(<span class="pl-k">var</span> c;c<span class="pl-k">=</span><span class="pl-v">this</span>.a[b];b<span class="pl-k">++</span>)<span class="pl-k">if</span>(c<span class="pl-k">==</span>a){b<span class="pl-k">=!</span><span class="pl-c1">0</span>;<span class="pl-k">break</span> a}b<span class="pl-k">=!</span><span class="pl-c1">1</span>}<span class="pl-k">if</span>(b)<span class="pl-k">return</span><span class="pl-k">!</span><span class="pl-c1">1</span>;<span class="pl-k">if</span>(<span class="pl-v">this</span>.d){<span class="pl-k">if</span>(<span class="pl-v">this</span>.r)c<span class="pl-k">=</span><span class="pl-v">this</span>.a.<span class="pl-c1">length</span><span class="pl-k">+</span><span class="pl-c1">1</span>,b<span class="pl-k">=</span>(<span class="pl-v">this</span>.d.lat()<span class="pl-k">*</span>(c<span class="pl-k">-</span><span class="pl-c1">1</span>)<span class="pl-k">+</span>a.getPosition().lat())/c,c<span class="pl-k">=</span>(<span class="pl-v">this</span>.d.lng()<span class="pl-k">*</span>(c<span class="pl-k">-</span><span class="pl-c1">1</span>)<span class="pl-k">+</span>a.getPosition().lng())/c,<span class="pl-v">this</span>.d<span class="pl-k">=</span><span class="pl-k">new</span> <span class="pl-en">google.maps</span>.LatLng(b,c),y(<span class="pl-v">this</span>)}<span class="pl-k">else</span> <span class="pl-v">this</span>.d<span class="pl-k">=</span>a.getPosition(),y(<span class="pl-v">this</span>);a.s<span class="pl-k">=!</span><span class="pl-c1">0</span>;<span class="pl-v">this</span>.a.<span class="pl-c1">push</span>(a);b<span class="pl-k">=</span><span class="pl-v">this</span>.a.<span class="pl-c1">length</span>;b<span class="pl-k">&lt;</span><span class="pl-v">this</span>.l<span class="pl-k">&amp;&amp;</span>a.getMap()<span class="pl-k">!=</span><span class="pl-v">this</span>.c<span class="pl-k">&amp;&amp;</span>a.setMap(<span class="pl-v">this</span>.c);<span class="pl-k">if</span>(b<span class="pl-k">==</span><span class="pl-v">this</span>.l)<span class="pl-k">for</span>(c<span class="pl-k">=</span><span class="pl-c1">0</span>;c<span class="pl-k">&lt;</span>b;c<span class="pl-k">++</span>)<span class="pl-v">this</span>.a[c].setMap(d);b<span class="pl-k">&gt;=</span><span class="pl-v">this</span>.l<span class="pl-k">&amp;&amp;</span>a.setMap(d);</td>
      </tr>
      <tr>
        <td id="L12" class="blob-num js-line-number" data-line-number="12"></td>
        <td id="LC12" class="blob-code blob-code-inner js-file-line">a<span class="pl-k">=</span><span class="pl-v">this</span>.c.getZoom();<span class="pl-k">if</span>((b<span class="pl-k">=</span><span class="pl-v">this</span>.k.I())<span class="pl-k">&amp;&amp;</span>a<span class="pl-k">&gt;</span>b)<span class="pl-k">for</span>(a<span class="pl-k">=</span><span class="pl-c1">0</span>;b<span class="pl-k">=</span><span class="pl-v">this</span>.a[a];a<span class="pl-k">++</span>)b.setMap(<span class="pl-v">this</span>.c);<span class="pl-k">else</span> <span class="pl-k">if</span>(<span class="pl-v">this</span>.a.<span class="pl-c1">length</span><span class="pl-k">&lt;</span><span class="pl-v">this</span>.l)z(<span class="pl-v">this</span>.n);<span class="pl-k">else</span>{b<span class="pl-k">=</span><span class="pl-v">this</span>.k.H()(<span class="pl-v">this</span>.a,<span class="pl-v">this</span>.k.<span class="pl-c1">z</span>().<span class="pl-c1">length</span>);<span class="pl-v">this</span>.n.setCenter(<span class="pl-v">this</span>.d);a<span class="pl-k">=</span><span class="pl-v">this</span>.n;a.B<span class="pl-k">=</span>b;a.ga<span class="pl-k">=</span>b.<span class="pl-c1">text</span>;a.ea<span class="pl-k">=</span>b.<span class="pl-c1">index</span>;<span class="pl-k">if</span>(a.b)a.b.innerHTML<span class="pl-k">=</span>b.<span class="pl-c1">text</span>;b<span class="pl-k">=</span><span class="pl-c1">Math</span>.<span class="pl-c1">max</span>(<span class="pl-c1">0</span>,a.B.<span class="pl-c1">index</span><span class="pl-k">-</span><span class="pl-c1">1</span>);b<span class="pl-k">=</span><span class="pl-c1">Math</span>.<span class="pl-c1">min</span>(a.j.<span class="pl-c1">length</span><span class="pl-k">-</span><span class="pl-c1">1</span>,b);b<span class="pl-k">=</span>a.j[b];a.da<span class="pl-k">=</span>b.url;a.h<span class="pl-k">=</span>b.<span class="pl-c1">height</span>;a.p<span class="pl-k">=</span>b.<span class="pl-c1">width</span>;a.M<span class="pl-k">=</span>b.textColor;a.e<span class="pl-k">=</span>b.anchor;a.N<span class="pl-k">=</span>b.textSize;a.D<span class="pl-k">=</span>b.backgroundPosition;<span class="pl-v">this</span>.n.show()}<span class="pl-k">return</span><span class="pl-k">!</span><span class="pl-c1">0</span>};</td>
      </tr>
      <tr>
        <td id="L13" class="blob-num js-line-number" data-line-number="13"></td>
        <td id="LC13" class="blob-code blob-code-inner js-file-line"><span class="pl-c1">j</span>.<span class="pl-en">getBounds</span><span class="pl-k">=</span><span class="pl-k">function</span>(){<span class="pl-k">for</span>(<span class="pl-k">var</span> a<span class="pl-k">=</span><span class="pl-k">new</span> <span class="pl-en">google.maps</span>.LatLngBounds(<span class="pl-v">this</span>.d,<span class="pl-v">this</span>.d),b<span class="pl-k">=</span><span class="pl-v">this</span>.o(),c<span class="pl-k">=</span><span class="pl-c1">0</span>,f;f<span class="pl-k">=</span>b[c];c<span class="pl-k">++</span>)a.extend(f.getPosition());<span class="pl-k">return</span> a};<span class="pl-c1">j</span>.<span class="pl-en">remove</span><span class="pl-k">=</span><span class="pl-k">function</span>(){<span class="pl-v">this</span>.n.remove();<span class="pl-v">this</span>.a.<span class="pl-c1">length</span><span class="pl-k">=</span><span class="pl-c1">0</span>;<span class="pl-k">delete</span> <span class="pl-v">this</span>.a};<span class="pl-c1">j</span>.<span class="pl-en">T</span><span class="pl-k">=</span><span class="pl-k">function</span>(){<span class="pl-k">return</span> <span class="pl-v">this</span>.a.<span class="pl-c1">length</span>};j.o<span class="pl-k">=</span>h(<span class="pl-s"><span class="pl-pds">&quot;</span>a<span class="pl-pds">&quot;</span></span>);j.getCenter<span class="pl-k">=</span>h(<span class="pl-s"><span class="pl-pds">&quot;</span>d<span class="pl-pds">&quot;</span></span>);<span class="pl-k">function</span> <span class="pl-en">y</span>(<span class="pl-smi">a</span>){a.F<span class="pl-k">=</span>a.k.v(<span class="pl-k">new</span> <span class="pl-en">google.maps</span>.LatLngBounds(a.d,a.d))}j.getMap<span class="pl-k">=</span>h(<span class="pl-s"><span class="pl-pds">&quot;</span>c<span class="pl-pds">&quot;</span></span>);</td>
      </tr>
      <tr>
        <td id="L14" class="blob-num js-line-number" data-line-number="14"></td>
        <td id="LC14" class="blob-code blob-code-inner js-file-line"><span class="pl-k">function</span> <span class="pl-en">t</span>(<span class="pl-smi">a</span>,<span class="pl-smi">b</span>,<span class="pl-smi">c</span>){a.k.extend(t,google.maps.OverlayView);<span class="pl-v">this</span>.j<span class="pl-k">=</span>b;<span class="pl-v">this</span>.fa<span class="pl-k">=</span>c<span class="pl-k">||</span><span class="pl-c1">0</span>;<span class="pl-v">this</span>.u<span class="pl-k">=</span>a;<span class="pl-v">this</span>.d<span class="pl-k">=</span>d;<span class="pl-v">this</span>.c<span class="pl-k">=</span>a.getMap();<span class="pl-v">this</span>.B<span class="pl-k">=</span><span class="pl-v">this</span>.b<span class="pl-k">=</span>d;<span class="pl-v">this</span>.t<span class="pl-k">=!</span><span class="pl-c1">1</span>;<span class="pl-v">this</span>.setMap(<span class="pl-v">this</span>.c)}j<span class="pl-k">=</span>t.<span class="pl-c1">prototype</span>;</td>
      </tr>
      <tr>
        <td id="L15" class="blob-num js-line-number" data-line-number="15"></td>
        <td id="LC15" class="blob-code blob-code-inner js-file-line"><span class="pl-c1">j</span>.<span class="pl-en">onAdd</span><span class="pl-k">=</span><span class="pl-k">function</span>(){<span class="pl-v">this</span>.b<span class="pl-k">=</span><span class="pl-c1">document</span>.<span class="pl-c1">createElement</span>(<span class="pl-s"><span class="pl-pds">&quot;</span>DIV<span class="pl-pds">&quot;</span></span>);<span class="pl-k">if</span>(<span class="pl-v">this</span>.t)<span class="pl-v">this</span>.b.<span class="pl-c1">style</span>.cssText<span class="pl-k">=</span>A(<span class="pl-v">this</span>,B(<span class="pl-v">this</span>,<span class="pl-v">this</span>.d)),<span class="pl-v">this</span>.b.innerHTML<span class="pl-k">=</span><span class="pl-v">this</span>.B.<span class="pl-c1">text</span>;<span class="pl-v">this</span>.getPanes().overlayMouseTarget.<span class="pl-c1">appendChild</span>(<span class="pl-v">this</span>.b);<span class="pl-k">var</span> a<span class="pl-k">=</span><span class="pl-v">this</span>;google.maps.<span class="pl-c1">event</span>.addDomListener(<span class="pl-v">this</span>.b,<span class="pl-s"><span class="pl-pds">&quot;</span>click<span class="pl-pds">&quot;</span></span>,<span class="pl-k">function</span>(){<span class="pl-k">var</span> b<span class="pl-k">=</span>a.u.k;google.maps.<span class="pl-c1">event</span>.trigger(b,<span class="pl-s"><span class="pl-pds">&quot;</span>clusterclick<span class="pl-pds">&quot;</span></span>,a.u);b.O<span class="pl-k">&amp;&amp;</span>a.c.fitBounds(a.u.getBounds())})};<span class="pl-k">function</span> <span class="pl-en">B</span>(<span class="pl-smi">a</span>,<span class="pl-smi">b</span>){<span class="pl-k">var</span> c<span class="pl-k">=</span>a.getProjection().fromLatLngToDivPixel(b);c.<span class="pl-c1">x</span><span class="pl-k">-=</span><span class="pl-c1">parseInt</span>(a.p/<span class="pl-c1">2</span>,<span class="pl-c1">10</span>);c.<span class="pl-c1">y</span><span class="pl-k">-=</span><span class="pl-c1">parseInt</span>(a.h/<span class="pl-c1">2</span>,<span class="pl-c1">10</span>);<span class="pl-k">return</span> c}</td>
      </tr>
      <tr>
        <td id="L16" class="blob-num js-line-number" data-line-number="16"></td>
        <td id="LC16" class="blob-code blob-code-inner js-file-line"><span class="pl-c1">j</span>.<span class="pl-en">draw</span><span class="pl-k">=</span><span class="pl-k">function</span>(){<span class="pl-k">if</span>(<span class="pl-v">this</span>.t){<span class="pl-k">var</span> a<span class="pl-k">=</span>B(<span class="pl-v">this</span>,<span class="pl-v">this</span>.d);<span class="pl-v">this</span>.b.<span class="pl-c1">style</span>.<span class="pl-c1">top</span><span class="pl-k">=</span>a.<span class="pl-c1">y</span><span class="pl-k">+</span><span class="pl-s"><span class="pl-pds">&quot;</span>px<span class="pl-pds">&quot;</span></span>;<span class="pl-v">this</span>.b.<span class="pl-c1">style</span>.<span class="pl-c1">left</span><span class="pl-k">=</span>a.<span class="pl-c1">x</span><span class="pl-k">+</span><span class="pl-s"><span class="pl-pds">&quot;</span>px<span class="pl-pds">&quot;</span></span>}};<span class="pl-k">function</span> <span class="pl-en">z</span>(<span class="pl-smi">a</span>){<span class="pl-k">if</span>(a.b)a.b.<span class="pl-c1">style</span>.<span class="pl-c1">display</span><span class="pl-k">=</span><span class="pl-s"><span class="pl-pds">&quot;</span>none<span class="pl-pds">&quot;</span></span>;a.t<span class="pl-k">=!</span><span class="pl-c1">1</span>}<span class="pl-c1">j</span>.<span class="pl-en">show</span><span class="pl-k">=</span><span class="pl-k">function</span>(){<span class="pl-k">if</span>(<span class="pl-v">this</span>.b)<span class="pl-v">this</span>.b.<span class="pl-c1">style</span>.cssText<span class="pl-k">=</span>A(<span class="pl-v">this</span>,B(<span class="pl-v">this</span>,<span class="pl-v">this</span>.d)),<span class="pl-v">this</span>.b.<span class="pl-c1">style</span>.<span class="pl-c1">display</span><span class="pl-k">=</span><span class="pl-s"><span class="pl-pds">&quot;</span><span class="pl-pds">&quot;</span></span>;<span class="pl-v">this</span>.t<span class="pl-k">=!</span><span class="pl-c1">0</span>};<span class="pl-c1">j</span>.<span class="pl-en">remove</span><span class="pl-k">=</span><span class="pl-k">function</span>(){<span class="pl-v">this</span>.setMap(d)};<span class="pl-c1">j</span>.<span class="pl-en">onRemove</span><span class="pl-k">=</span><span class="pl-k">function</span>(){<span class="pl-k">if</span>(<span class="pl-v">this</span>.b<span class="pl-k">&amp;&amp;</span><span class="pl-v">this</span>.b.<span class="pl-c1">parentNode</span>)z(<span class="pl-v">this</span>),<span class="pl-v">this</span>.b.<span class="pl-c1">parentNode</span>.removeChild(<span class="pl-v">this</span>.b),<span class="pl-v">this</span>.b<span class="pl-k">=</span>d};j.setCenter<span class="pl-k">=</span>e(<span class="pl-s"><span class="pl-pds">&quot;</span>d<span class="pl-pds">&quot;</span></span>);</td>
      </tr>
      <tr>
        <td id="L17" class="blob-num js-line-number" data-line-number="17"></td>
        <td id="LC17" class="blob-code blob-code-inner js-file-line"><span class="pl-k">function</span> <span class="pl-en">A</span>(<span class="pl-smi">a</span>,<span class="pl-smi">b</span>){<span class="pl-k">var</span> c<span class="pl-k">=</span>[];c.<span class="pl-c1">push</span>(<span class="pl-s"><span class="pl-pds">&quot;</span>background-image:url(<span class="pl-pds">&quot;</span></span><span class="pl-k">+</span>a.da<span class="pl-k">+</span><span class="pl-s"><span class="pl-pds">&quot;</span>);<span class="pl-pds">&quot;</span></span>);c.<span class="pl-c1">push</span>(<span class="pl-s"><span class="pl-pds">&quot;</span>background-position:<span class="pl-pds">&quot;</span></span><span class="pl-k">+</span>(a.D<span class="pl-k">?</span>a.D<span class="pl-k">:</span><span class="pl-s"><span class="pl-pds">&quot;</span>0 0<span class="pl-pds">&quot;</span></span>)<span class="pl-k">+</span><span class="pl-s"><span class="pl-pds">&quot;</span>;<span class="pl-pds">&quot;</span></span>);<span class="pl-k">typeof</span> a.e<span class="pl-k">===</span><span class="pl-s"><span class="pl-pds">&quot;</span>object<span class="pl-pds">&quot;</span></span><span class="pl-k">?</span>(<span class="pl-k">typeof</span> a.e[<span class="pl-c1">0</span>]<span class="pl-k">===</span><span class="pl-s"><span class="pl-pds">&quot;</span>number<span class="pl-pds">&quot;</span></span><span class="pl-k">&amp;&amp;</span>a.e[<span class="pl-c1">0</span>]<span class="pl-k">&gt;</span><span class="pl-c1">0</span><span class="pl-k">&amp;&amp;</span>a.e[<span class="pl-c1">0</span>]<span class="pl-k">&lt;</span>a.h<span class="pl-k">?</span>c.<span class="pl-c1">push</span>(<span class="pl-s"><span class="pl-pds">&quot;</span>height:<span class="pl-pds">&quot;</span></span><span class="pl-k">+</span>(a.h<span class="pl-k">-</span>a.e[<span class="pl-c1">0</span>])<span class="pl-k">+</span><span class="pl-s"><span class="pl-pds">&quot;</span>px; padding-top:<span class="pl-pds">&quot;</span></span><span class="pl-k">+</span>a.e[<span class="pl-c1">0</span>]<span class="pl-k">+</span><span class="pl-s"><span class="pl-pds">&quot;</span>px;<span class="pl-pds">&quot;</span></span>)<span class="pl-k">:</span>c.<span class="pl-c1">push</span>(<span class="pl-s"><span class="pl-pds">&quot;</span>height:<span class="pl-pds">&quot;</span></span><span class="pl-k">+</span>a.h<span class="pl-k">+</span><span class="pl-s"><span class="pl-pds">&quot;</span>px; line-height:<span class="pl-pds">&quot;</span></span><span class="pl-k">+</span>a.h<span class="pl-k">+</span><span class="pl-s"><span class="pl-pds">&quot;</span>px;<span class="pl-pds">&quot;</span></span>),<span class="pl-k">typeof</span> a.e[<span class="pl-c1">1</span>]<span class="pl-k">===</span><span class="pl-s"><span class="pl-pds">&quot;</span>number<span class="pl-pds">&quot;</span></span><span class="pl-k">&amp;&amp;</span>a.e[<span class="pl-c1">1</span>]<span class="pl-k">&gt;</span><span class="pl-c1">0</span><span class="pl-k">&amp;&amp;</span>a.e[<span class="pl-c1">1</span>]<span class="pl-k">&lt;</span>a.p<span class="pl-k">?</span>c.<span class="pl-c1">push</span>(<span class="pl-s"><span class="pl-pds">&quot;</span>width:<span class="pl-pds">&quot;</span></span><span class="pl-k">+</span>(a.p<span class="pl-k">-</span>a.e[<span class="pl-c1">1</span>])<span class="pl-k">+</span><span class="pl-s"><span class="pl-pds">&quot;</span>px; padding-left:<span class="pl-pds">&quot;</span></span><span class="pl-k">+</span>a.e[<span class="pl-c1">1</span>]<span class="pl-k">+</span><span class="pl-s"><span class="pl-pds">&quot;</span>px;<span class="pl-pds">&quot;</span></span>)<span class="pl-k">:</span>c.<span class="pl-c1">push</span>(<span class="pl-s"><span class="pl-pds">&quot;</span>width:<span class="pl-pds">&quot;</span></span><span class="pl-k">+</span>a.p<span class="pl-k">+</span><span class="pl-s"><span class="pl-pds">&quot;</span>px; text-align:center;<span class="pl-pds">&quot;</span></span>))<span class="pl-k">:</span>c.<span class="pl-c1">push</span>(<span class="pl-s"><span class="pl-pds">&quot;</span>height:<span class="pl-pds">&quot;</span></span><span class="pl-k">+</span>a.h<span class="pl-k">+</span><span class="pl-s"><span class="pl-pds">&quot;</span>px; line-height:<span class="pl-pds">&quot;</span></span><span class="pl-k">+</span>a.h<span class="pl-k">+</span></td>
      </tr>
      <tr>
        <td id="L18" class="blob-num js-line-number" data-line-number="18"></td>
        <td id="LC18" class="blob-code blob-code-inner js-file-line"><span class="pl-s"><span class="pl-pds">&quot;</span>px; width:<span class="pl-pds">&quot;</span></span><span class="pl-k">+</span>a.p<span class="pl-k">+</span><span class="pl-s"><span class="pl-pds">&quot;</span>px; text-align:center;<span class="pl-pds">&quot;</span></span>);c.<span class="pl-c1">push</span>(<span class="pl-s"><span class="pl-pds">&quot;</span>cursor:pointer; top:<span class="pl-pds">&quot;</span></span><span class="pl-k">+</span>b.<span class="pl-c1">y</span><span class="pl-k">+</span><span class="pl-s"><span class="pl-pds">&quot;</span>px; left:<span class="pl-pds">&quot;</span></span><span class="pl-k">+</span>b.<span class="pl-c1">x</span><span class="pl-k">+</span><span class="pl-s"><span class="pl-pds">&quot;</span>px; color:<span class="pl-pds">&quot;</span></span><span class="pl-k">+</span>(a.M<span class="pl-k">?</span>a.M<span class="pl-k">:</span><span class="pl-s"><span class="pl-pds">&quot;</span>black<span class="pl-pds">&quot;</span></span>)<span class="pl-k">+</span><span class="pl-s"><span class="pl-pds">&quot;</span>; position:absolute; font-size:<span class="pl-pds">&quot;</span></span><span class="pl-k">+</span>(a.N<span class="pl-k">?</span>a.N<span class="pl-k">:</span><span class="pl-c1">11</span>)<span class="pl-k">+</span><span class="pl-s"><span class="pl-pds">&quot;</span>px; font-family:Arial,sans-serif; font-weight:bold<span class="pl-pds">&quot;</span></span>);<span class="pl-k">return</span> c.<span class="pl-c1">join</span>(<span class="pl-s"><span class="pl-pds">&quot;</span><span class="pl-pds">&quot;</span></span>)}<span class="pl-c1">window</span>.MarkerClusterer<span class="pl-k">=</span>k;<span class="pl-c1">k</span>.<span class="pl-c1">prototype</span>.<span class="pl-en">addMarker</span><span class="pl-k">=</span>k.<span class="pl-c1">prototype</span>.q;<span class="pl-c1">k</span>.<span class="pl-c1">prototype</span>.<span class="pl-en">addMarkers</span><span class="pl-k">=</span>k.<span class="pl-c1">prototype</span>.C;<span class="pl-c1">k</span>.<span class="pl-c1">prototype</span>.<span class="pl-en">clearMarkers</span><span class="pl-k">=</span>k.<span class="pl-c1">prototype</span>.R;<span class="pl-c1">k</span>.<span class="pl-c1">prototype</span>.<span class="pl-en">fitMapToMarkers</span><span class="pl-k">=</span>k.<span class="pl-c1">prototype</span>.S;<span class="pl-c1">k</span>.<span class="pl-c1">prototype</span>.<span class="pl-en">getCalculator</span><span class="pl-k">=</span>k.<span class="pl-c1">prototype</span>.H;<span class="pl-c1">k</span>.<span class="pl-c1">prototype</span>.<span class="pl-en">getGridSize</span><span class="pl-k">=</span>k.<span class="pl-c1">prototype</span>.w;</td>
      </tr>
      <tr>
        <td id="L19" class="blob-num js-line-number" data-line-number="19"></td>
        <td id="LC19" class="blob-code blob-code-inner js-file-line"><span class="pl-c1">k</span>.<span class="pl-c1">prototype</span>.<span class="pl-en">getExtendedBounds</span><span class="pl-k">=</span>k.<span class="pl-c1">prototype</span>.v;<span class="pl-c1">k</span>.<span class="pl-c1">prototype</span>.<span class="pl-en">getMap</span><span class="pl-k">=</span>k.<span class="pl-c1">prototype</span>.getMap;<span class="pl-c1">k</span>.<span class="pl-c1">prototype</span>.<span class="pl-en">getMarkers</span><span class="pl-k">=</span>k.<span class="pl-c1">prototype</span>.o;<span class="pl-c1">k</span>.<span class="pl-c1">prototype</span>.<span class="pl-en">getMaxZoom</span><span class="pl-k">=</span>k.<span class="pl-c1">prototype</span>.I;<span class="pl-c1">k</span>.<span class="pl-c1">prototype</span>.<span class="pl-en">getStyles</span><span class="pl-k">=</span>k.<span class="pl-c1">prototype</span>.<span class="pl-c1">z</span>;<span class="pl-c1">k</span>.<span class="pl-c1">prototype</span>.<span class="pl-en">getTotalClusters</span><span class="pl-k">=</span>k.<span class="pl-c1">prototype</span>.U;<span class="pl-c1">k</span>.<span class="pl-c1">prototype</span>.<span class="pl-en">getTotalMarkers</span><span class="pl-k">=</span>k.<span class="pl-c1">prototype</span>.V;<span class="pl-c1">k</span>.<span class="pl-c1">prototype</span>.<span class="pl-en">redraw</span><span class="pl-k">=</span>k.<span class="pl-c1">prototype</span>.i;<span class="pl-c1">k</span>.<span class="pl-c1">prototype</span>.<span class="pl-en">removeMarker</span><span class="pl-k">=</span>k.<span class="pl-c1">prototype</span>.Y;<span class="pl-c1">k</span>.<span class="pl-c1">prototype</span>.<span class="pl-en">removeMarkers</span><span class="pl-k">=</span>k.<span class="pl-c1">prototype</span>.Z;<span class="pl-c1">k</span>.<span class="pl-c1">prototype</span>.<span class="pl-en">resetViewport</span><span class="pl-k">=</span>k.<span class="pl-c1">prototype</span>.m;<span class="pl-c1">k</span>.<span class="pl-c1">prototype</span>.<span class="pl-en">repaint</span><span class="pl-k">=</span>k.<span class="pl-c1">prototype</span>.L;<span class="pl-c1">k</span>.<span class="pl-c1">prototype</span>.<span class="pl-en">setCalculator</span><span class="pl-k">=</span>k.<span class="pl-c1">prototype</span>.$;</td>
      </tr>
      <tr>
        <td id="L20" class="blob-num js-line-number" data-line-number="20"></td>
        <td id="LC20" class="blob-code blob-code-inner js-file-line"><span class="pl-c1">k</span>.<span class="pl-c1">prototype</span>.<span class="pl-en">setGridSize</span><span class="pl-k">=</span>k.<span class="pl-c1">prototype</span>.aa;<span class="pl-c1">k</span>.<span class="pl-c1">prototype</span>.<span class="pl-en">setMaxZoom</span><span class="pl-k">=</span>k.<span class="pl-c1">prototype</span>.ba;<span class="pl-c1">k</span>.<span class="pl-c1">prototype</span>.<span class="pl-en">onAdd</span><span class="pl-k">=</span>k.<span class="pl-c1">prototype</span>.onAdd;<span class="pl-c1">k</span>.<span class="pl-c1">prototype</span>.<span class="pl-en">draw</span><span class="pl-k">=</span>k.<span class="pl-c1">prototype</span>.draw;<span class="pl-c1">s</span>.<span class="pl-c1">prototype</span>.<span class="pl-en">getCenter</span><span class="pl-k">=</span>s.<span class="pl-c1">prototype</span>.getCenter;<span class="pl-c1">s</span>.<span class="pl-c1">prototype</span>.<span class="pl-en">getSize</span><span class="pl-k">=</span>s.<span class="pl-c1">prototype</span>.T;<span class="pl-c1">s</span>.<span class="pl-c1">prototype</span>.<span class="pl-en">getMarkers</span><span class="pl-k">=</span>s.<span class="pl-c1">prototype</span>.o;<span class="pl-c1">t</span>.<span class="pl-c1">prototype</span>.<span class="pl-en">onAdd</span><span class="pl-k">=</span>t.<span class="pl-c1">prototype</span>.onAdd;<span class="pl-c1">t</span>.<span class="pl-c1">prototype</span>.<span class="pl-en">draw</span><span class="pl-k">=</span>t.<span class="pl-c1">prototype</span>.draw;<span class="pl-c1">t</span>.<span class="pl-c1">prototype</span>.<span class="pl-en">onRemove</span><span class="pl-k">=</span>t.<span class="pl-c1">prototype</span>.onRemove;</td>
      </tr>
      <tr>
        <td id="L21" class="blob-num js-line-number" data-line-number="21"></td>
        <td id="LC21" class="blob-code blob-code-inner js-file-line">})();</td>
      </tr>
</table>

  </div>

</div>

<a href="#jump-to-line" rel="facebox[.linejump]" data-hotkey="l" style="display:none">Jump to Line</a>
<div id="jump-to-line" style="display:none">
  <form accept-charset="UTF-8" action="" class="js-jump-to-line-form" method="get"><div style="margin:0;padding:0;display:inline"><input name="utf8" type="hidden" value="&#x2713;" /></div>
    <input class="linejump-input js-jump-to-line-field" type="text" placeholder="Jump to line&hellip;" autofocus>
    <button type="submit" class="btn">Go</button>
</form></div>

        </div>

      </div><!-- /.repo-container -->
      <div class="modal-backdrop"></div>
    </div><!-- /.container -->
  </div><!-- /.site -->


    </div><!-- /.wrapper -->

      <div class="container">
  <div class="site-footer" role="contentinfo">
    <ul class="site-footer-links right">
        <li><a href="https://status.github.com/" data-ga-click="Footer, go to status, text:status">Status</a></li>
      <li><a href="https://developer.github.com" data-ga-click="Footer, go to api, text:api">API</a></li>
      <li><a href="https://training.github.com" data-ga-click="Footer, go to training, text:training">Training</a></li>
      <li><a href="https://shop.github.com" data-ga-click="Footer, go to shop, text:shop">Shop</a></li>
        <li><a href="https://github.com/blog" data-ga-click="Footer, go to blog, text:blog">Blog</a></li>
        <li><a href="https://github.com/about" data-ga-click="Footer, go to about, text:about">About</a></li>
        <li><a href="https://help.github.com" data-ga-click="Footer, go to help, text:help">Help</a></li>

    </ul>

    <a href="https://github.com" aria-label="Homepage">
      <span class="mega-octicon octicon-mark-github" title="GitHub"></span>
</a>
    <ul class="site-footer-links">
      <li>&copy; 2015 <span title="0.04520s from github-fe131-cp1-prd.iad.github.net">GitHub</span>, Inc.</li>
        <li><a href="https://github.com/site/terms" data-ga-click="Footer, go to terms, text:terms">Terms</a></li>
        <li><a href="https://github.com/site/privacy" data-ga-click="Footer, go to privacy, text:privacy">Privacy</a></li>
        <li><a href="https://github.com/security" data-ga-click="Footer, go to security, text:security">Security</a></li>
        <li><a href="https://github.com/contact" data-ga-click="Footer, go to contact, text:contact">Contact</a></li>
    </ul>
  </div>
</div>


    <div class="fullscreen-overlay js-fullscreen-overlay" id="fullscreen_overlay">
  <div class="fullscreen-container js-suggester-container">
    <div class="textarea-wrap">
      <textarea name="fullscreen-contents" id="fullscreen-contents" class="fullscreen-contents js-fullscreen-contents" placeholder=""></textarea>
      <div class="suggester-container">
        <div class="suggester fullscreen-suggester js-suggester js-navigation-container"></div>
      </div>
    </div>
  </div>
  <div class="fullscreen-sidebar">
    <a href="#" class="exit-fullscreen js-exit-fullscreen tooltipped tooltipped-w" aria-label="Exit Zen Mode">
      <span class="mega-octicon octicon-screen-normal"></span>
    </a>
    <a href="#" class="theme-switcher js-theme-switcher tooltipped tooltipped-w"
      aria-label="Switch themes">
      <span class="octicon octicon-color-mode"></span>
    </a>
  </div>
</div>



    
    

    <div id="ajax-error-message" class="flash flash-error">
      <span class="octicon octicon-alert"></span>
      <a href="#" class="octicon octicon-x flash-close js-ajax-error-dismiss" aria-label="Dismiss error"></a>
      Something went wrong with that request. Please try again.
    </div>


      <script crossorigin="anonymous" src="https://assets-cdn.github.com/assets/frameworks-3241a40a58a82e21daef3dd3cdca01bde189158793c1b6f9193fff2b5293cd1d.js"></script>
      <script async="async" crossorigin="anonymous" src="https://assets-cdn.github.com/assets/github/index-60b249427d9766f9f7c2ce367b03a9ed485faded0f6ebc2be69b8442d789d8db.js"></script>
      
      
  </body>
</html>

