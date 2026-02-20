/* 
  Add these CSS rules to frontend/styles.css for feed management UI
*/

/* Feed Manager Section */
.feed-manager {
    margin: 15px 0;
    padding: 10px;
    border: 1px solid #2fd0ff;
    border-radius: 4px;
    background: rgba(47, 208, 255, 0.05);
}

.add-feed-btn {
    width: 100%;
    padding: 10px;
    background: #0f1318;
    border: 1px solid #2fd0ff;
    color: #2fd0ff;
    font-family: 'Share Tech Mono', monospace;
    font-weight: bold;
    cursor: pointer;
    border-radius: 3px;
    transition: all 0.3s ease;
}

.add-feed-btn:hover {
    background: #2fd0ff;
    color: #0f1318;
    text-shadow: 0 0 10px rgba(47, 208, 255, 0.5);
}

/* Feed List */
.feed-list {
    margin-top: 10px;
    max-height: 300px;
    overflow-y: auto;
}

.feed-item {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 8px;
    margin: 5px 0;
    background: rgba(47, 208, 255, 0.1);
    border-radius: 3px;
    font-size: 11px;
    border-left: 3px solid #2fd0ff;
}

.feed-name {
    flex: 1;
    padding-left: 8px;
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
    color: #7ee7ff;
}

.delete-btn {
    background: rgba(255, 50, 50, 0.2);
    border: 1px solid #ff3232;
    color: #ff3232;
    width: 24px;
    height: 24px;
    padding: 0;
    margin-left: 8px;
    cursor: pointer;
    border-radius: 3px;
    font-weight: bold;
    transition: all 0.3s ease;
    font-family: monospace;
}

.delete-btn:hover {
    background: #ff3232;
    color: #0f1318;
}

/* Status Indicator */
#status {
    display: inline-block;
    padding: 5px 10px;
    border-radius: 3px;
    font-size: 12px;
    font-weight: bold;
    margin-right: 10px;
}

#status.connected {
    color: #00ff00;
    border: 1px solid #00ff00;
}

#status.disconnected {
    color: #ff5555;
    border: 1px solid #ff5555;
}

#status.error {
    color: #ff9900;
    border: 1px solid #ff9900;
}

/* Article Styling */
.article {
    margin: 10px 0;
    padding: 12px;
    border-left: 4px solid #2fd0ff;
    background: rgba(47, 208, 255, 0.05);
    border-radius: 3px;
}

.article[data-severity="critical"] {
    border-left-color: #ff0000;
}

.article[data-severity="high"] {
    border-left-color: #ff5555;
}

.article[data-severity="medium"] {
    border-left-color: #ffaa00;
}

.article[data-severity="low"] {
    border-left-color: #00ff00;
}

.article-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 8px;
    font-size: 11px;
    gap: 10px;
}

.source {
    font-weight: bold;
    flex: 0 0 auto;
}

.category {
    background: rgba(47, 208, 255, 0.2);
    padding: 2px 6px;
    border-radius: 2px;
    font-size: 10px;
}

.severity {
    padding: 2px 6px;
    border-radius: 2px;
    font-weight: bold;
    font-size: 10px;
}

.severity-critical {
    background: #ff0000;
    color: white;
}

.severity-high {
    background: #ff5555;
    color: white;
}

.severity-medium {
    background: #ffaa00;
    color: #0f1318;
}

.severity-low {
    background: #00ff00;
    color: #0f1318;
}

.article-title {
    font-weight: bold;
    margin-bottom: 6px;
    color: #7ee7ff;
    word-break: break-word;
}

.article-summary {
    font-size: 12px;
    color: #aaaaaa;
    margin-bottom: 8px;
    line-height: 1.4;
}

.article-footer {
    display: flex;
    justify-content: space-between;
    align-items: center;
    font-size: 11px;
}

.article-link {
    color: #00ff00;
    text-decoration: none;
    font-weight: bold;
    cursor: pointer;
}

.article-link:hover {
    text-decoration: underline;
    color: #7ee7ff;
}

.timestamp {
    color: #666666;
    font-size: 10px;
}

.no-articles {
    padding: 20px;
    text-align: center;
    color: #666666;
    font-style: italic;
}
