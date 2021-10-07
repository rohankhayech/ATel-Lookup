export class ColorUtilities {
  public static stringToColor(s: string) {
    return `#${this.numberToColor(this.hashString(s))}`;
  }

  private static hashString(s: string) {
    let hash = 0;

    for (let i = 0; i < s.length; i++) {
      hash = s.charCodeAt(i) + ((hash << 5) - hash);
    }

    return hash;
  }

  private static numberToColor(n: number) {
    var c = (n & 0x00ffffff).toString(16).toUpperCase();

    return '00000'.substring(0, 6 - c.length) + c;
  }
}
