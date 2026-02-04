// safety.js
// Client-side safety, rate limiting, and sanitisation for the Noventrax Cyberskills Assistant

const MAX_MESSAGE_LENGTH = 500;
const MIN_MESSAGE_INTERVAL_MS = 3000; // 3 seconds

const CYBERSEC_UNSAFE_PATTERNS = [
    /ddos/i,
    /\bDDoS\b/i,
    /botnet/i,
    /ransomware/i,
    /zero[-\s]?day/i,
    /exploit code/i,
    /malware sample/i,
    /payload/i,
    /sql injection/i,
    /\bsqli\b/i,
    /xss payload/i,
    /\bbruteforce\b/i,
    /credential stuffing/i
];

const GENERIC_UNSAFE_PATTERNS = [
    /kill/i,
    /suicide/i,
    /self[-\s]?harm/i
];

let lastMessageTimestamp = 0;

function sanitizeInput(text) {
    if (!text) return "";
    return text.replace(/</g, "&lt;").replace(/>/g, "&gt;");
}

function sanitizeOutput(text) {
    if (!text) return "";
    return text.replace(/</g, "&lt;").replace(/>/g, "&gt;");
}

function isValidMessage(text) {
    if (!text || text.trim() === "") {
        return { ok: false, reason: "empty" };
    }
    if (text.length > MAX_MESSAGE_LENGTH) {
        return { ok: false, reason: "too_long" };
    }
    return { ok: true };
}

function containsUnsafeContent(text) {
    if (!text) return false;
    const patterns = [...CYBERSEC_UNSAFE_PATTERNS, ...GENERIC_UNSAFE_PATTERNS];
    return patterns.some((re) => re.test(text));
}

function canSendMessageNow() {
    const now = Date.now();
    if (now - lastMessageTimestamp < MIN_MESSAGE_INTERVAL_MS) {
        return {
            ok: false,
            retryAfterMs: MIN_MESSAGE_INTERVAL_MS - (now - lastMessageTimestamp)
        };
    }
    lastMessageTimestamp = now;
    return { ok: true };
}

// expose as global
window.Safety = {
    sanitizeInput,
    sanitizeOutput,
    isValidMessage,
    containsUnsafeContent,
    canSendMessageNow
};

