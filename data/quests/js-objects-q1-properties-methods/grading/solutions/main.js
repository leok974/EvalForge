export const person = {
    firstName: "John",
    lastName: "Doe",
    fullName() {
        return `${this.firstName} ${this.lastName}`;
    }
};