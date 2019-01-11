/**
 * 颜色处理工具包
 */

/**
 * 调整rgb颜色亮度
 * @param color 要调整的 rgb 值，格式 rgb(a,b,c)
 * @param percent 要调整的百分比，取值范围[0,1]
 *        正值表示调亮（向白端调整）, 传入 +1 会得到 rgb(255,255,255)
 *        负值表示调暗（向黑端调整）, 传入 -1 会得到 rgb(0,0,0)
 * @example shadeRGBColor('rgb(100,100,100)',0.3) => 'rgb(147,147,147)'
 * thanks to pimp-trizkit(https://stackoverflow.com/users/693927/pimp-trizkit)
 * @see https://stackoverflow.com/questions/5560248/programmatically-lighten-or-darken-a-hex-color-or-rgb-and-blend-colors
 */
export function shadeRGBColor(color: string, percent: number) {
    const f = color.split(","), t = percent < 0 ? 0 : 255, p = percent < 0 ? percent * -1 : percent,
        R = parseInt(f[0].slice(4)), G = parseInt(f[1]), B = parseInt(f[2]);
    return "rgb(" + (Math.round((t - R) * p) + R) + "," + (Math.round((t - G) * p) + G) + "," + (Math.round((t - B) * p) + B) + ")";
}

/**
 * 调整 hex 格式颜色亮度
 * @param color 要调整的 hex 颜色值，格式 rgb(a,b,c)
 * @param percent 要调整的百分比，取值范围[0,1]
 *        正值表示调亮（向白端调整）, 传入 +1 会得到 #ffffff
 *        负值表示调暗（向黑端调整）, 传入 -1 会得到 #000000
 * @example shadeHexColor("#aaaaaa",0.3) => 'rgb(147,147,147)'
 * thanks to pimp-trizkit(https://stackoverflow.com/users/693927/pimp-trizkit)
 * @see https://stackoverflow.com/questions/5560248/programmatically-lighten-or-darken-a-hex-color-or-rgb-and-blend-colors
 */
function shadeHexColor(color: string, percent: number) {
    const f = parseInt(color.slice(1), 16), t = percent < 0 ? 0 : 255, p = percent < 0 ? percent * -1 : percent,
        R = f >> 16, G = f >> 8 & 0x00FF, B = f & 0x0000FF;
    return "#" + (0x1000000 + (Math.round((t - R) * p) + R) * 0x10000 + (Math.round((t - G) * p) + G) * 0x100 + (Math.round((t - B) * p) + B)).toString(16).slice(1);
}

/**
 * 根据传入参数 color 自动选择 shadeRGBColor 或 shadeHexColor
 */
export function shade(color: string, percent: number) {
    if (color.length > '#xxxxxx'.length) return shadeRGBColor(color, percent);
    else return shadeHexColor(color, percent);
}

export const BEAUTIFUL_LIGHT_COLOR = [
    '#0099FF',
    '#6699FF',
    '#99CCFF',
    '#CC99FF',
    '#66FF99',
    '#99FF99',
    '#CC9999',
    '#FF9999',
    '#FFCC99',
    '#FF6699'
];