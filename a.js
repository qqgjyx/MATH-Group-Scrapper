<!DOCTYPE html>
<html lang="en">
 <head>
  <meta charset="utf-8"/>
  <meta content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=0" name="viewport"/>
  <meta content="DSMZ cultivation media database" name="description"/>
  <meta content="Julia Koblitz" name="author"/>
  <!-- Open Graph / Facebook -->
  <meta content="https://mediadive.dsmz.de" property="og:url">
   <meta content="database" property="og:type">
    <meta content="Heyndrickxia coagulans DSM 1 | Strains | MediaDive" property="og:title">
     <meta content="Discover standardized cultivation media recipes for more than 40,000 microbial strains." property="og:description">
      <meta content="/img/mediadive_logo.svg" property="og:image"/>
      <!-- Twitter -->
      <meta content="summary_large_image" property="twitter:card"/>
      <meta content="https://mediadive.dsmz.de" property="twitter:url"/>
      <meta content="MediaDive — the cultivation media database" property="twitter:title"/>
      <meta content="Discover standardized cultivation media recipes for more than 40,000 microbial strains." property="twitter:description"/>
      <meta content="/img/mediadive_avatar.png" property="twitter:image"/>
      <link href="/img/favicon.png" rel="icon"/>
      <title>
       Heyndrickxia coagulans DSM 1 | Strains | MediaDive
      </title>
      <!-- Phosphoricons and individual D3 icons -->
      <link href="/css/phosphoricons/regular/style.css" rel="stylesheet">
       <link href="/css/phosphoricons/fill/style.css" rel="stylesheet"/>
       <link href="/css/d3icons/style.css?v=2" rel="stylesheet"/>
       <link href="/css/digidive.css?v=3" rel="stylesheet"/>
       <link href="/css/shepherd.css" rel="stylesheet"/>
       <link href="/css/animate.min.css" rel="stylesheet"/>
       <link href="/css/jquery-ui.min.css" rel="stylesheet"/>
       <link href="/css/style.css?1698918304" rel="stylesheet"/>
       <script>
        // define global constants
        const ROOTPATH = "";
       </script>
       <script src="/js/jquery-3.3.1.min.js">
       </script>
       <script src="/js/jquery-ui.min.js">
       </script>
       <!-- Requires digidive.js for the dropdowns -->
       <!-- <script src="/js/digidive.js"></script> -->
       <script src="/js/digidive.js?v=3">
       </script>
       <script src="/js/script.js?1698918307">
       </script>
       <!-- Matomo -->
       <script>
        var _paq = window._paq = window._paq || [];
            /* tracker methods like "setCustomDimension" should be called before "trackPageView" */
            _paq.push(['trackPageView']);
            _paq.push(['enableLinkTracking']);
            (function() {
                var u = "https://piwik.dsmz.de/";
                _paq.push(['setTrackerUrl', u + 'matomo.php']);
                _paq.push(['setSiteId', '15']);
                var d = document,
                    g = d.createElement('script'),
                    s = d.getElementsByTagName('script')[0];
                g.async = true;
                g.src = u + 'matomo.js';
                s.parentNode.insertBefore(g, s);
            })();
       </script>
       <noscript>
        <p>
         <img alt="" src="https://piwik.dsmz.de/matomo.php?idsite=15&amp;rec=1" style="border:0;"/>
        </p>
       </noscript>
       <!-- End Matomo Code -->
      </link>
     </meta>
    </meta>
   </meta>
  </meta>
 </head>
 <body style="position: relative">
  <!-- Modals go here -->
  <!-- <div class="modal modal-lg" id="settings" tabindex="-1" role="dialog">
    <div class="modal-dialog" role="document">
        <div class="modal-content w-400 mw-full">
            <a href="#" class="btn float-right" role="button" aria-label="Close">
                <span aria-hidden="true">&times;</span>
            </a>
            <h5 class="title"><i class="ph ph-gear text-primary"></i> Settings</h5>

            <form action="#" method="get">

                <div class="form-group">
                    <label for="language">Language</label>
                    <select name="language" id="language" class="form-control">
                        <option value="en" selected>English</option>
                        <option value="de" >Deutsch</option>
                    </select>
                </div>

                <div class="form-group">
                    <div class="custom-checkbox">
                        <input type="checkbox" id="transitions" name="transitions" value="true" >
                        <label for="transitions">Motion-sickness mode</label><br>
                        <small class="text-muted">This mode reduces motion and animations on the page.</small>
                    </div>
                </div>
                <div class="form-group">
                    <div class="custom-checkbox">
                        <input type="checkbox" id="dyslexia" name="dyslexia" value="true" >
                        <label for="dyslexia">Dyslexia mode</label><br>
                        <small class="text-muted">
                            The web page uses a special font to increase readibility for user with dyslexia.                        </small>
                    </div>
                </div>
                <p>
                    We use browser cookies to save your preferences.                </p>
                <button class="btn primary">Apply</button>
            </form>

        </div>
    </div>
</div> -->
  <div class="modal modal-lg" id="ingredient-modal" role="dialog" tabindex="-1">
   <div class="modal-dialog" role="document">
    <div class="modal-content">
     <a aria-label="Close" class="btn float-right" href="#" onclick="digidive.toggleModal('ingredient-modal')" role="button">
      <span aria-hidden="true">
       ×
      </span>
     </a>
     <h5 class="title">
      Ingredient name
     </h5>
     <div id="ingredient-content">
     </div>
    </div>
   </div>
  </div>
  <div class="modal modal-lg" id="universal-modal" role="dialog" tabindex="-1">
   <div class="modal-dialog" role="document">
    <div class="modal-content">
     <a aria-label="Close" class="btn float-right" href="#" onclick="digidive.toggleModal('universal-modal')" role="button">
      <span aria-hidden="true">
       ×
      </span>
     </a>
     <div class="content" id="universal-content">
     </div>
    </div>
   </div>
  </div>
  <div class="loader">
   <span>
   </span>
  </div>
  <div class="popup-bg" onclick="hidePopups();">
  </div>
  <!-- Page wrapper start -->
  <div class="page-wrapper">
   <!-- data-sidebar-hidden to hide sidebar on start -->
   <!-- Sticky alerts (toasts), empty container -->
   <div class="sticky-alerts">
   </div>
   <!-- Sidebar overlay -->
   <div class="sidebar-overlay" onclick="digidive.toggleSidebar()">
   </div>
   <!-- Navbar start -->
   <div class="navbar navbar-top">
    <div class="container">
     <!-- here goes your database logo -->
     <a class="navbar-brand position-relative" href="/">
      <img alt="MediaDive" class="" src="/img/mediadive_logo.svg" style="width: 30rem;"/>
     </a>
     <a class="navbar-brand ml-auto d-none d-sm-block" href="//www.dsmz.de/">
      <!-- DSMZ Logo is mandatory -->
      <img alt="DSMZ" src="/img/dsmz_full.svg"/>
     </a>
    </div>
   </div>
   <nav class="navbar navbar-bottom">
    <!-- Button to toggle sidebar -->
    <div class="container">
     <button class="btn btn-action active" onclick="digidive.toggleSidebar(this);" type="button">
     </button>
     <ul class="navbar-nav">
      <nav aria-label="MediaDive breadcrumbs">
       <ul class="breadcrumb m-0">
        <li>
         <a href="/">
          Home
         </a>
        </li>
        <li>
         <a href="/strains">
          Strains
         </a>
        </li>
        <li aria-current="page" class="active">
         <a href="javascript:void(0)">
          Heyndrickxia coagulans DSM 1
         </a>
        </li>
       </ul>
      </nav>
     </ul>
     <div class="dropdown">
      <button aria-expanded="false" aria-haspopup="true" class="btn accessibility" data-toggle="dropdown" id="accessibility-menu" type="button">
       <span class="sr-only">
        Accessibility Options
       </span>
      </button>
      <div aria-labelledby="accessibility-menu" class="dropdown-menu dropdown-menu-center w-300">
       <h6 class="header text-primary">
        Accessibility
       </h6>
       <form action="#" class="content" method="get">
        <input name="accessibility[check]" type="hidden"/>
        <div class="form-group">
         <label for="language">
          Language
         </label>
         <select class="form-control" id="language" name="accessibility[language]">
          <option selected="" value="en">
           English
          </option>
          <option value="de">
           Deutsch
          </option>
         </select>
        </div>
        <div class="form-group">
         <div class="custom-checkbox">
          <input id="set-contrast" name="accessibility[contrast]" type="checkbox" value="high-contrast"/>
          <label for="set-contrast">
           High contrast
          </label>
          <br/>
          <small class="text-muted">
           Enhance the contrast of the web page for better readability.
          </small>
         </div>
        </div>
        <div class="form-group">
         <div class="custom-checkbox">
          <input id="set-transitions" name="accessibility[transitions]" type="checkbox" value="without-transitions"/>
          <label for="set-transitions">
           Reduce motion
          </label>
          <br/>
          <small class="text-muted">
           Reduce motion and animations on the page.
          </small>
         </div>
        </div>
        <div class="form-group">
         <div class="custom-checkbox">
          <input id="set-dyslexia" name="accessibility[dyslexia]" type="checkbox" value="dyslexia"/>
          <label for="set-dyslexia">
           Dyslexia mode
          </label>
          <br/>
          <small class="text-muted">
           Use a special font to increase readability for users with dyslexia.
          </small>
         </div>
        </div>
        <button class="btn primary">
         Apply
        </button>
       </form>
      </div>
     </div>
     <form action="/media" class="nav-search" id="medium-search" method="get">
      <div class="input-group">
       <input autocomplete="off" class="form-control" name="search" placeholder="Search medium" type="text"/>
       <div class="input-group-append">
        <button class="btn primary">
         <i aria-hidden="true" class="ph ph-magnifying-glass">
         </i>
        </button>
       </div>
      </div>
      <div class="suggestions">
      </div>
     </form>
    </div>
   </nav>
   <!-- Sidebar start -->
   <div class="sidebar">
    <nav class="sidebar-topnav">
     <ul>
      <li>
       <a href="/docs">
        <i class="ph ph-book">
        </i>
        Manual
       </a>
      </li>
      <li>
       <a href="/con-form" title="Support">
        <i class="ph ph-headset">
        </i>
        Support
       </a>
      </li>
     </ul>
    </nav>
    <div class="sidebar-menu">
     <!-- Sidebar links (with icons) and titles -->
     <h5 class="title">
      Content
     </h5>
     <a class="with-icon danger" href="/media">
      <i aria-hidden="true" class="ph ph-flask">
      </i>
      Media
     </a>
     <a class="with-icon primary" href="/solutions">
      <i aria-hidden="true" class="ph ph-test-tube">
      </i>
      Solutions
     </a>
     <a class="with-icon success" href="/ingredients">
      <i aria-hidden="true" class="ph ph-mortar-pestle">
      </i>
      Ingredients
     </a>
     <a class="with-icon signal active" href="/strains">
      <!-- text-white bg-dark text-dark-dm bg-light-dm -->
      <i aria-hidden="true" class="ph ph-microbes">
      </i>
      Strains
     </a>
     <a class="with-icon" href="/steps">
      <i aria-hidden="true" class="ph ph-list-checks">
      </i>
      Steps
     </a>
     <a class="with-icon" href="/gas">
      <i aria-hidden="true" class="ph ph-gas">
      </i>
      Gas
     </a>
     <h5 class="title">
      Search
     </h5>
     <a class="with-icon" href="/finder">
      <i aria-hidden="true" class="ph ph-target">
      </i>
      Medium finder
     </a>
     <a class="with-icon" href="/solution-finder">
      <i aria-hidden="true" class="ph ph-magnifying-glass-plus">
      </i>
      Solution finder
     </a>
     <a class="with-icon" href="/taxonomy">
      <i aria-hidden="true" class="ph ph-taxonomy">
      </i>
      Taxonomy search
     </a>
     <a class="with-icon" href="/isolation-sources">
      <i aria-hidden="true" class="ph ph-map-pin-line">
      </i>
      Isolation sources
     </a>
     <h5 class="title">
      Tools
     </h5>
     <a class="with-icon" href="/medium-builder">
      <i aria-hidden="true" class="ph ph-flask-pen">
      </i>
      Medium builder
      <span class="badge badge-success ml-5">
       NEW
      </span>
     </a>
     <a class="with-icon" href="/unit-converter">
      <i aria-hidden="true" class="ph ph-arrows-clockwise">
      </i>
      Unit converter
     </a>
     <a class="with-icon" href="/compare-media">
      <i aria-hidden="true" class="ph ph-flask-vial">
      </i>
      Compare media
     </a>
     <a class="with-icon" href="/compare-solutions">
      <i aria-hidden="true" class="ph ph-vials">
      </i>
      Compare solutions
     </a>
     <a class="with-icon" href="/prediction">
      <i aria-hidden="true" class="ph ph-chip-ai">
      </i>
      Prediction
      <span class="badge badge-primary ml-5">
       SOON
      </span>
     </a>
     <div class="sidebar-content text-muted d-block d-sm-none">
      <!-- brought to you by -->
      <a class="navbar-brand ml-auto pb-10" href="//www.dsmz.de/">
       <!-- DSMZ Logo is mandatory -->
       <img alt="DSMZ" src="/img/dsmz_full.svg"/>
      </a>
     </div>
    </div>
   </div>
   <div class="content-wrapper">
    <div class="content-container">
     <a id="top">
     </a>
     <div class="content">
      <a class="btn" href="/strains?">
       <i class="ph ph-caret-left">
       </i>
       Back to all strains
      </a>
      <div class="float-right">
       <a class="" href="https://www.dsmz.de/collection/catalogue/details/culture/DSM-1" target="_blank">
        <img alt="DSMZ" src="/img/dsmz_small.svg" style="height:3rem;"/>
       </a>
       <a class="" href="https://bacdive.dsmz.de/strain/654" target="_blank">
        <img alt="BacDive" src="/img/bacdive_small.svg" style="height:3rem;"/>
       </a>
      </div>
      <h2>
       Heyndrickxia coagulans DSM 1
      </h2>
      <span class="badge">
       <span title="Bacteria">
        <i class="ph ph-lg ph-streptococcus text-danger">
        </i>
       </span>
       Bacterium
      </span>
      <p>
       <b>
        Synonyms:
       </b>
       ATCC 7050, BCRC 10606, CCM 2013, CCUG 7417, CECT 12, CFBP 4225, CIP 66.25, CN 2202,
       <a href="https://www.dsmz.de/collection/catalogue/details/culture/DSM-1" target="_blank">
        DSM 1
       </a>
       , HAMBI 1931, IAM 1115, IAM 12463, IFO 12583, IMET 10993,
       <a href="https://www.jcm.riken.jp/cgi-bin/jcm/jcm_number?DSM=1" target="_blank">
        JCM 2257
       </a>
       , KCTC 3625, LMG 6326, NBRC 12583, NCCB 77025, NCFB 1761, NCIB 9365, NCIMB 9365, NCTC 10334, NRIC 1005, NRRL NRS-609, NRS 609, VKM B-497, VTT E-98150, WDCM 00002
      </p>
     </div>
     <div class="content">
      <div class="box">
       <div class="content">
        <h3 class="title">
         <a class="link colorless" href="/medium/1?ccno=DSM 1">
          1: NUTRIENT AGAR
         </a>
        </h3>
       </div>
       <hr/>
       <div class="content">
        <p>
         <b class="mr-10">
          Growth observed:
         </b>
         <i class="ph ph-lg ph-check text-success">
         </i>
        </p>
        <p>
         <b class="mr-10">
          Growth conditions:
         </b>
         <span class="badge danger" data-title="Optimum temperature" data-toggle="tooltip">
          40 °C
         </span>
        </p>
       </div>
      </div>
      <div class="box">
       <div class="content">
        <h3 class="title">
         <a class="link colorless" href="/medium/453?ccno=DSM 1">
          453: STANDARD I MEDIUM
         </a>
        </h3>
       </div>
       <hr/>
       <div class="content">
        <p>
         <b class="mr-10">
          Growth observed:
         </b>
         <i class="ph ph-lg ph-check text-success">
         </i>
        </p>
        <p>
         <b class="mr-10">
          Growth conditions:
         </b>
         <span class="badge danger" data-title="Optimum temperature" data-toggle="tooltip">
          40 °C
         </span>
        </p>
       </div>
      </div>
      <div class="box">
       <div class="content">
        <h3 class="title">
         <a class="link colorless" href="/medium/J22?ccno=DSM 1">
          J22: NUTRIENT AGAR NO. 2
         </a>
        </h3>
       </div>
       <hr/>
       <div class="content">
        <p>
         <b class="mr-10">
          Growth observed:
         </b>
         <i class="ph ph-lg ph-check text-success">
         </i>
        </p>
        <p>
        </p>
       </div>
      </div>
     </div>
     <script>
      function filldata(growth_id = null) {
        // clear the form
        var form = $('form#strain-form')
        form.find('input:not([type=hidden],[type=checkbox],[type=radio])').val('')
        form.find('select option[value=""]').prop('selected', true)

        // if the add button was pushed: nothing more to do
        if (growth_id === null) return;

        // select growth data from json input
        var jsonString = $('#strain-data-' + growth_id).html()
        var json = JSON.parse(jsonString)
        console.log(json);

        // enter input fields
        for (const name in json) {
            const input = form.find('[name=' + (name == 'medium_id' ? 'medium' : name) + ']')
            if (Object.hasOwnProperty.call(json, name) && input.length !== 0) {
                const value = json[name];
                const type = input.attr('type')
                console.log(name);
                if (type == 'select') {
                    input.find('option[value="' + value + '"]').prop('selected', true)
                } else if (type == 'checkbox') {
                    input.prop('checked', value)
                } else if (type == 'radio') {
                    form.find('[name=' + name + '][value=' + value + ']')
                        .prop('checked', true)
                } else {
                    input.val(value)
                }
            }
        }
    }
     </script>
     <div class="position-absolute top-0 right-0 z-30" id="cookieWarning">
      <div class="alert primary filled-dm w-300 w-sm-500 w-md-600" role="alert">
       <div class="row align-items-center">
        <div class="col-sm-2">
         <div class="w-100 h-100 d-flex align-items-center rounded-circle bg-white mx-auto">
          <div class="m-auto">
           <i aria-hidden="true" class="ph ph-cookie ph-4x" style="color: #6F4E37;">
           </i>
          </div>
         </div>
        </div>
        <div class="col-sm-9 offset-sm-1 py-10">
         <h4 class="title">
          Have some cookies!
         </h4>
         We are using cookies to improve the user experience. We save the following information: user preferences for language, accessibility, help features and medium favourites. Unfortunately, you cannot use this site if you don't agree.
         <div class="mb-10 text-right">
          <button class="btn alt-dm" onclick="acceptCookies();">
           I agree
          </button>
         </div>
        </div>
       </div>
      </div>
     </div>
    </div>
    <footer class="page-footer">
     <!--
  <div class="footer text-center">

    <div class="w-500 mw-full mx-auto my-20">
      <h3 class="mt-0">
        Did not found what you were looking for?      </h3>
      <div class="input-group">
        <input type="search" name="search" id="hub-search" class="form-control" placeholder="Search across all DSMZ Digital Diversity databases">
        <div class="input-group-append">
          <button class="btn"><i class="ph ph-magnifying-glass" aria-hidden="true"></i></button>
        </div>
      </div>
    </div>
  </div>

  <hr> -->
     <div class="link-parade">
      <div class="row">
       <div class="col">
        <h3>
         Media
         <em>
          Dive
         </em>
        </h3>
        <a href="/about">
         About
        </a>
        <a href="/news">
         News
        </a>
        <a href="http://dx.doi.org/10.1093/nar/gkac803" target="_blank">
         Cite
        </a>
        <a href="/stats">
         Statistics
        </a>
       </div>
       <div class="col">
        <h3>
         Help
        </h3>
        <a href="/docs/website">
         Website
        </a>
        <a href="/docs/medium-builder">
         Medium builder
        </a>
        <a href="/doc/index.html">
         API reference
        </a>
        <a href="/con-form">
         Support
        </a>
       </div>
       <div class="col">
        <h3>
         Social Media
        </h3>
        <a href="https://twitter.com/DSMZMediaDive" target="_blank">
         <span class="icon">
          <i class="ph ph-twitter-logo">
          </i>
         </span>
         @DSMZMediaDive
        </a>
        <a href="https://www.youtube.com/channel/UCZxfaPawuEmsNNInlIf1Pbw" target="_blank">
         <span class="icon">
          <i class="ph ph-youtube-logo">
          </i>
         </span>
         YouTube
        </a>
       </div>
      </div>
     </div>
     <!-- <div class="logo-parade">
    <a href="javascript:void(0)"><img src="https://bacdive.dsmz.de/images/logo/deNBI_Logo_rgb.svg" alt=""></a>
    <a href="javascript:void(0)"><img src="https://bacdive.dsmz.de/images/logo/CoreData_Logo_clean.svg" alt=""></a>

</div> -->
     <hr/>
     <div class="footer">
      <span>
       © DSMZ 2024
      </span>
      <a href="/imprint">
       Imprint
      </a>
      <a href="/imprint#privacy">
       Privacy Statement
      </a>
      <a href="/imprint#license">
       <img alt="" src="/img/cc.svg" style="height:1.3em;vertical-align:text-bottom;"/>
       <img alt="" src="/img/by.svg" style="height:1.3em;vertical-align:text-bottom;"/>
       License
      </a>
      <a href="/sitemap.xml">
       Sitemap
      </a>
     </div>
    </footer>
   </div>
  </div>
  <!-- <div class="swipe-area"></div> -->
  <script>
   function acceptCookies() {
    digidive.createCookie("bacmedia-cookie-seen", true)
    $("#cookieWarning").hide()
  }
  </script>
  <script src="/js/tour/popper.min.js">
  </script>
  <script src="/js/tour/shepherd.min.js">
  </script>
  <script src="/js/tour/tour.js?1698918307">
  </script>
  <script src="/js/tour/tour_strains.js?1698918307">
  </script>
 </body>
</html>
