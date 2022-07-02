export function URLify(string) {
    // Replace whitespace with -
    let s = string.trim().replace(/\s/g, '-');
    return s.toLowerCase()
}
