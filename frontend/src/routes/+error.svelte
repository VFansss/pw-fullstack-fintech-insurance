<script context="module" lang="ts">
  export const prerender = true;
</script>

<svelte:head>
  <title>404 - Page Not Found</title>
</svelte:head>

<div class="error-page">
  <span class="neg">404 MEDITATION</span>

  <p>
    The most beautiful things are those that madness prompts and reason writes.
    <br />
    <br />
    ~ Jim Morrison
  </p>

  <p>
    * This page is not where you expect it to be<br />
    * But don't panic, keep calm<br />
    * Take a deep breath<br />
  </p>

  Press any link to continue<span class="blink">_</span>

  <br /><br />

  <div>
    <a href="/">Return Home</a> |
    <a href="https://en.wikipedia.org/wiki/Special:Random">Learn Something New</a> |
    <a href="https://www.youtube.com">Watch YouTube</a>
  </div>
</div>

<style>
  .error-page {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: #0000aa;
    color: #ffffff;
    font-family: courier;
    font-size: 12pt;
    text-align: center;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
  }
  .neg {
    background: #fff;
    color: #0000aa;
    padding: 2px 8px;
    font-weight: bold;
  }
  p {
    margin: 30px 100px;
  }
  a,
  a:hover {
    color: inherit;
    font: inherit;
    text-decoration: none;
  }
  a:hover {
    text-decoration: underline;
  }
  .blink {
    animation: 1s blinker linear infinite;
    -webkit-animation: 1s blinker linear infinite;
    -moz-animation: 1s blinker linear infinite;
    color: white;
  }
  @keyframes blinker {
    0% {
      opacity: 1;
    }
    50% {
      opacity: 0;
    }
    100% {
      opacity: 1;
    }
  }
</style>
