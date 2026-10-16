#ifndef EX3_HP_H
#define EX3_HP_H

#include <iostream>
#include <sstream>
using std::ostream;

#define DEFAULT_MAX_HP 100

class HealthPoints {

public:
    /*
     * C'tor of HealthPoints class
     *
     * @param maxHP - The maximum amount and starting health of the
     *                character (defaulted at 100).
     * @return
     *      A new instance of HealthPoints
     */
    HealthPoints(const int maxHP = DEFAULT_MAX_HP);

    /*
     * +/- operator for changing the value of the current HP
     *
     * @param amount - The amount of health to add/subtract from this instance's value
     * @return
     *      A new object containing the same stats as this instance's values, +/- the
     *      given amount, bounded by 0 and maxHP
     */
    HealthPoints operator+(const int amount) const;
    HealthPoints operator-(const int amount) const;

    /*
     * Same function as the + operator above but in [int + HealthPoints] input format
     *
     * @param amount - The amount of health to add from the given instance's value
     * @param HP - The HealthPoints instance to refer in the adding operation
     * @return
     *      A new object containing the same stats as the given instance's values,
     *      + the given amount, bounded by 0 and maxHP
     */
    friend HealthPoints operator+(const int amount, const HealthPoints& HP);

    /*
     * Same funciton as the +/- operators but acting on this instance insted of returning
     * a new instance
     *
     * @param amount - The amount of health to add/subtract from this instance's value
     * @return
     *      void
     */
    void operator+=(const int amount);
    void operator-=(const int amount);

    /*
     * Compare ==/!= operator to detemine if two HealthPoints instances has the same HP value
     *
     * @param other - The other HealthPoints instance to compare HP values with
     * @return
     *      true - if both instances has the equal HP in == and not equal HP in !=
     *      false - elsewise
     */
    bool operator==(const HealthPoints& other) const;
    bool operator!=(const HealthPoints& other) const;

    /*
     * Compare >=/>/<=/< operator to detemine the relation between two HealthPoints instances'
     * values of HP
     *
     * @param other - The other HealthPoints instance to compare HP values with
     * @return
     *      true - if the relevant operator is correct relative to the recived instance
     *      false - elsewise
     */
    bool operator>=(const HealthPoints& other) const;
    bool operator>(const HealthPoints& other) const;
    bool operator<=(const HealthPoints& other) const;
    bool operator<(const HealthPoints& other) const;

    /*
     * Overloading of << operator to print it to given std ostream
     *
     * @param stream - The std ostream to be printed to
     * @param HP - The HealthPoints instace to be printed to the stream
     * @return
     *      the received ostream to allow this operator's concatenation
     */
    friend ostream& operator<<(ostream& stream, const HealthPoints& HP);

    /*
     * An exception to be thrown when the class c'tor is called with an invalid
     * (non-positive) value
     */
    class InvalidArgument {
    };

    /*
     * Default copy c'tor, d'tor and = operator
     */
    HealthPoints(const HealthPoints& other) = default;
    ~HealthPoints() = default;
    HealthPoints& operator=(const HealthPoints& other) = default;

private:
    int m_maxHP;
    int m_HP;
};

#endif // EX3_HP_H
