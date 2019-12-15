export const USER_NOT_FOUND = 'USER_NOT_FOUND'
export const EMAIL_ALREADY_USED = 'EMAIL_ALREADY_USED'
export const NON_EXISTENT = (entity: 'match' | 'persona'| 'club' | 'league' | 'news') => `NON_EXISTENT_${entity.toUpperCase()}`
