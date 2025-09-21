function getVisibleText() {
  const walker = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT, {
    acceptNode: function(node) {
      if (!node.parentElement || window.getComputedStyle(node.parentElement).display === 'none' || window.getComputedStyle(node.parentElement).visibility === 'hidden') {
        return NodeFilter.FILTER_REJECT;
      }
      if (node.textContent.trim() === '') {
        return NodeFilter.FILTER_REJECT;
      }
      return NodeFilter.FILTER_ACCEPT;
    }
  });
  let node;
  let text = '';
  while (node = walker.nextNode()) {
    text += node.textContent + ' ';
  }
  return text.trim();
}

chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
  if (request.action === 'getPageText') {
    const pageText = getVisibleText();
    sendResponse({ text: pageText });
  }
});