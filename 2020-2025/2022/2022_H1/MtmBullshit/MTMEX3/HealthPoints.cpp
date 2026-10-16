#include "HealthPoints.h"

HealthPoints::HealthPoints(const int maxHP)
{
    if (maxHP <= 0) {
        throw InvalidArgument();
    }
    m_maxHP = maxHP;
    m_HP = maxHP;
}

HealthPoints HealthPoints::operator+(const int amount) const
{
    HealthPoints out(m_maxHP);
    out.m_HP += amount;

    if (out.m_HP > m_maxHP) {
        out.m_HP = m_maxHP;
    }

    if (out.m_HP < 0) {
        out.m_HP = 0;
    }

    return out;
}

HealthPoints HealthPoints::operator-(const int amount) const
{
    return *this + (-amount);
}

HealthPoints operator+(const int amount, const HealthPoints& HP)
{
    return HP + amount;
}

void HealthPoints::operator+=(const int amount)
{
    *this = *this + amount;
}

void HealthPoints::operator-=(const int amount)
{
    *this = *this - amount;
}

bool HealthPoints::operator==(const HealthPoints& other) const
{
    return m_HP == other.m_HP;
}

bool HealthPoints::operator!=(const HealthPoints& other) const
{
    return m_HP != other.m_HP;
}

bool HealthPoints::operator>=(const HealthPoints& other) const
{
    return m_HP >= other.m_HP;
}

bool HealthPoints::operator>(const HealthPoints& other) const
{
    return m_HP > other.m_HP;
}

bool HealthPoints::operator<=(const HealthPoints& other) const
{
    return m_HP <= other.m_HP;
}

bool HealthPoints::operator<(const HealthPoints& other) const
{
    return m_HP < other.m_HP;
}

ostream& operator<<(ostream& stream, const HealthPoints& HP)
{
    stream << HP.m_HP << "(" << HP.m_maxHP << ")";
    return stream;
}
