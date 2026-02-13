export interface Shape {
    area(): number;
}

export class Circle implements Shape {
    constructor(private radius: number) {}
    
    area(): number {
        return Math.PI * this.radius * this.radius;
    }
}