/**
 * Parses a fractional odds string (e.g. "6/4") into a decimal multiplier.
 * The decimal represents the profit per unit staked (e.g. 6/4 = 1.5x profit).
 */
function parseOdds(oddsString: string): number {
  const [numerator, denominator] = oddsString.split('/').map(Number)
  if (isNaN(numerator) || isNaN(denominator) || denominator === 0) {
    throw new Error(`Invalid odds string: "${oddsString}"`)
  }
  return numerator / denominator
}

/**
 * Calculates the Expected Value (EV) of a bet.
 *
 * @param oddsString - Fractional odds string, e.g. "6/4"
 * @param probability - Your estimated probability of winning, e.g. 0.53
 * @returns EV as a decimal (e.g. 0.15 means 15% return per unit staked)
 *
 * Formula: EV = (p * decimalOdds) - (1 - p)
 */
export function expectedValue(oddsString: string, probability: number): number {
  if (probability < 0 || probability > 1) {
    throw new Error('Probability must be between 0 and 1')
  }
  const decimalOdds = parseOdds(oddsString)
  return probability * decimalOdds - (1 - probability)
}

/**
 * Calculates the Kelly Criterion — the optimal fraction of your bankroll to stake.
 *
 * @param oddsString - Fractional odds string, e.g. "6/4"
 * @param probability - Your estimated probability of winning, e.g. 0.53
 * @returns Kelly fraction (e.g. 0.10 means stake 10% of bankroll).
 *          Returns 0 if the bet has no positive edge.
 *
 * Formula: f* = (b*p - q) / b
 *   where b = decimal odds, p = win probability, q = 1 - p
 */
export function kellyCriterion(
  oddsString: string,
  probability: number,
): number {
  if (probability < 0 || probability > 1) {
    throw new Error('Probability must be between 0 and 1')
  }
  const b = parseOdds(oddsString)
  const p = probability
  const q = 1 - probability
  const kelly = (b * p - q) / b
  return Math.max(0, kelly) // Never bet a negative fraction
}

export function toPercent(value: number): string {
  return `${(value * 100).toFixed(1)}%`
}
