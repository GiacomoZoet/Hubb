-- ============================================================
-- iMessageU — Full Database Schema
-- ============================================================

-- ============================================================
-- USERS
-- ============================================================
CREATE TABLE users (
    id          INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    username    VARCHAR(50) NOT NULL UNIQUE,
    email       VARCHAR(100) NOT NULL UNIQUE,
    password    VARCHAR(255) NOT NULL,
    avatar_url  VARCHAR(500) DEFAULT NULL,
    is_active   BOOLEAN DEFAULT TRUE,
    confirmed   BOOLEAN DEFAULT FALSE,
    last_seen   DATETIME DEFAULT NULL,
    created_at  DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- ============================================================
-- WORKSPACES
-- ============================================================
CREATE TABLE workspaces (
    id          INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    name        VARCHAR(100) NOT NULL,
    slug        VARCHAR(100) NOT NULL UNIQUE,
    owner_id    INT UNSIGNED NOT NULL,
    created_at  DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (owner_id) REFERENCES users(id) ON DELETE CASCADE
);

-- ============================================================
-- WORKSPACE MEMBERS
-- ============================================================
CREATE TABLE workspace_members (
    workspace_id    INT UNSIGNED NOT NULL,
    user_id         INT UNSIGNED NOT NULL,
    role            ENUM('owner', 'admin', 'member') DEFAULT 'member',
    joined_at       DATETIME DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (workspace_id, user_id),
    FOREIGN KEY (workspace_id) REFERENCES workspaces(id) ON DELETE CASCADE,
    FOREIGN KEY (user_id)      REFERENCES users(id) ON DELETE CASCADE
);

-- ============================================================
-- CHANNELS
-- ============================================================
CREATE TABLE channels (
    id              INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    workspace_id    INT UNSIGNED NOT NULL,
    name            VARCHAR(100) NOT NULL,
    description     VARCHAR(255) DEFAULT NULL,
    is_private      BOOLEAN DEFAULT FALSE,
    created_by      INT UNSIGNED DEFAULT NULL,
    created_at      DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (workspace_id) REFERENCES workspaces(id) ON DELETE CASCADE,
    FOREIGN KEY (created_by)   REFERENCES users(id) ON DELETE SET NULL
);

-- ============================================================
-- CHANNEL MEMBERS (private channels only)
-- ============================================================
CREATE TABLE channel_members (
    channel_id  INT UNSIGNED NOT NULL,
    user_id     INT UNSIGNED NOT NULL,
    PRIMARY KEY (channel_id, user_id),
    FOREIGN KEY (channel_id) REFERENCES channels(id) ON DELETE CASCADE,
    FOREIGN KEY (user_id)    REFERENCES users(id) ON DELETE CASCADE
);

-- ============================================================
-- MESSAGES
-- ============================================================
CREATE TABLE messages (
    id          INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    channel_id  INT UNSIGNED NOT NULL,
    user_id     INT UNSIGNED NOT NULL,
    content     TEXT NOT NULL,
    parent_id   INT UNSIGNED DEFAULT NULL,
    is_edited   BOOLEAN DEFAULT FALSE,
    created_at  DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (channel_id) REFERENCES channels(id) ON DELETE CASCADE,
    FOREIGN KEY (user_id)    REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (parent_id)  REFERENCES messages(id) ON DELETE SET NULL,
    FULLTEXT INDEX ft_content (content),
    INDEX idx_channel_created (channel_id, created_at)
);

-- ============================================================
-- DIRECT MESSAGES
-- ============================================================
CREATE TABLE direct_messages (
    id          INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    sender_id   INT UNSIGNED NOT NULL,
    receiver_id INT UNSIGNED NOT NULL,
    content     TEXT NOT NULL,
    is_read     BOOLEAN DEFAULT FALSE,
    created_at  DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (sender_id)   REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (receiver_id) REFERENCES users(id) ON DELETE CASCADE,
    INDEX idx_dm_users (sender_id, receiver_id)
);

-- ============================================================
-- ATTACHMENTS (channel messages + DMs)
-- ============================================================
CREATE TABLE attachments (
    id          INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    message_id  INT UNSIGNED DEFAULT NULL,
    dm_id       INT UNSIGNED DEFAULT NULL,
    file_url    VARCHAR(500) NOT NULL,
    file_name   VARCHAR(255) NOT NULL,
    file_type   VARCHAR(50) NOT NULL,
    file_size   INT UNSIGNED NOT NULL,
    uploaded_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (message_id) REFERENCES messages(id) ON DELETE CASCADE,
    FOREIGN KEY (dm_id)      REFERENCES direct_messages(id) ON DELETE CASCADE,
    CONSTRAINT chk_attachment CHECK (
        (message_id IS NOT NULL AND dm_id IS NULL) OR
        (message_id IS NULL AND dm_id IS NOT NULL)
    )
);

-- ============================================================
-- REACTIONS
-- ============================================================
CREATE TABLE reactions (
    id          INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    message_id  INT UNSIGNED NOT NULL,
    user_id     INT UNSIGNED NOT NULL,
    emoji       VARCHAR(10) NOT NULL,
    UNIQUE KEY unique_reaction (message_id, user_id, emoji),
    FOREIGN KEY (message_id) REFERENCES messages(id) ON DELETE CASCADE,
    FOREIGN KEY (user_id)    REFERENCES users(id) ON DELETE CASCADE
);

-- ============================================================
-- WORKSPACE INVITATIONS
-- ============================================================
CREATE TABLE workspace_invitations (
    id           INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    workspace_id INT UNSIGNED NOT NULL,
    invited_by   INT UNSIGNED NOT NULL,
    user_id      INT UNSIGNED NOT NULL,
    status       ENUM('pending', 'accepted', 'declined') DEFAULT 'pending',
    created_at   DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (workspace_id) REFERENCES workspaces(id) ON DELETE CASCADE,
    FOREIGN KEY (invited_by)   REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (user_id)      REFERENCES users(id) ON DELETE CASCADE
);

-- ============================================================
-- REFRESH TOKENS
-- ============================================================
CREATE TABLE refresh_tokens (
    id          INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    user_id     INT UNSIGNED NOT NULL,
    token       VARCHAR(500) NOT NULL UNIQUE,
    expires_at  DATETIME NOT NULL,
    revoked     BOOLEAN DEFAULT FALSE,
    created_at  DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);
