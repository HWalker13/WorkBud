"""Phase 6: Celery task — weekly avatar degradation + stat reset."""


def run_weekly_reset():
    """
    Scheduled weekly via Celery beat.
    For each user:
      - Compare workouts completed vs goal
      - Degrade avatar_state if goal not met (min 0)
      - Create WeeklyStat record for the closing week
      - Reset for the new week
    """
    raise NotImplementedError("Weekly reset not implemented until Phase 6")
