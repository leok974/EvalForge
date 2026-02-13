export const CONFIG = { env: "dev" };

export default function run(): string {
    return `Running in ${CONFIG.env}`;
}